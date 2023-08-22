"""Client for the AEMET OpenData REST API."""

import logging

from typing import Any, cast

from aiohttp import ClientError, ClientSession
from aiohttp.client_reqrep import ClientResponse
import geopy.distance
from geopy.distance import Distance

from .const import (
    AEMET_ATTR_DATA,
    AEMET_ATTR_STATION_LATITUDE,
    AEMET_ATTR_STATION_LONGITUDE,
    AEMET_ATTR_TOWN_LATITUDE_DECIMAL,
    AEMET_ATTR_TOWN_LONGITUDE_DECIMAL,
    AEMET_ATTR_WEATHER_STATION_LATITUDE,
    AEMET_ATTR_WEATHER_STATION_LONGITUDE,
    API_MIN_STATION_DISTANCE_KM,
    API_MIN_TOWN_DISTANCE_KM,
    API_TIMEOUT,
    API_URL,
    ATTR_DATA,
    ATTR_RESPONSE,
)
from .exceptions import AemetError, AuthError, TooManyRequests
from .helpers import parse_station_coordinates, parse_town_code

_LOGGER = logging.getLogger(__name__)


class AEMET:
    """Interacts with the AEMET OpenData API."""

    def __init__(
        self,
        aiohttp_session: ClientSession,
        api_key: str,
        timeout: int = API_TIMEOUT,
    ) -> None:
        """Init AEMET OpenData API."""
        self.aiohttp_session = aiohttp_session
        self.dist_hp: bool = False
        self.headers: dict[str, Any] = {
            "Cache-Control": "no-cache",
            "api_key": api_key,
        }
        self.timeout: int = timeout

    async def api_call(self, cmd: str, fetch_data: bool = False) -> dict[str, Any]:
        """Perform Rest API call."""
        _LOGGER.debug("api_call: cmd=%s", cmd)

        try:
            resp: ClientResponse = await self.aiohttp_session.request(
                "GET",
                f"{API_URL}/{cmd}",
                timeout=self.timeout,
                headers=self.headers,
            )
        except ClientError as err:
            raise AemetError(err) from err

        if resp.status == 401:
            raise AuthError(await resp.text())
        if resp.status == 429:
            raise TooManyRequests(await resp.text())
        if resp.status != 200:
            raise AemetError(f"API status={resp.status} text={await resp.text()}")

        resp_json = await resp.json(content_type=None)
        _LOGGER.debug("api_call: cmd=%s resp=%s", cmd, resp_json)

        json_response = cast(dict[str, Any], resp_json)
        if fetch_data and AEMET_ATTR_DATA in json_response:
            data = await self.api_data(json_response[AEMET_ATTR_DATA])
            if data:
                json_response = {
                    ATTR_RESPONSE: json_response,
                    ATTR_DATA: data,
                }
        if isinstance(json_response, list):
            json_response = {
                ATTR_DATA: json_response,
            }

        return json_response

    async def api_data(self, url: str) -> dict[str, Any]:
        """Fetch API data."""
        _LOGGER.debug("api_data: url=%s", url)

        try:
            resp: ClientResponse = await self.aiohttp_session.request(
                "GET",
                url,
                timeout=self.timeout,
            )
        except ClientError as err:
            raise AemetError(err) from err

        if resp.status != 200:
            raise AemetError(f"API status={resp.status} text={await resp.text()}")

        resp_json = await resp.json(content_type=None)
        _LOGGER.debug("api_data: url=%s resp=%s", url, resp_json)

        return cast(dict[str, Any], resp_json)

    def calc_distance(
        self, start: tuple[float, float], end: tuple[float, float]
    ) -> Distance:
        """Calculate distance between 2 points."""
        if self.dist_hp:
            return geopy.distance.geodesic(start, end)
        return geopy.distance.great_circle(start, end)

    def distance_high_precision(self, dist_hp: bool) -> bool:
        """Enable/Disable high precision for distance calculations."""
        self.dist_hp = dist_hp
        return self.dist_hp

    async def get_climatological_values_stations(
        self, fetch_data: bool = True
    ) -> dict[str, Any]:
        """Get stations available for climatological values."""
        return await self.api_call(
            "valores/climatologicos/inventarioestaciones/todasestaciones", fetch_data
        )

    async def get_climatological_values_station_by_coordinates(
        self, latitude: float, longitude: float
    ) -> dict[str, Any] | None:
        """Get closest climatological values station to coordinates."""
        stations = await self.get_climatological_values_stations()
        search_coords = (latitude, longitude)
        station = None
        distance = API_MIN_STATION_DISTANCE_KM
        for cur_station in stations[ATTR_DATA]:
            station_coords = parse_station_coordinates(
                cur_station[AEMET_ATTR_WEATHER_STATION_LATITUDE],
                cur_station[AEMET_ATTR_WEATHER_STATION_LONGITUDE],
            )
            station_point = geopy.point.Point(station_coords)
            cur_coords = (station_point.latitude, station_point.longitude)
            cur_distance = self.calc_distance(search_coords, cur_coords).km
            if cur_distance < distance:
                distance = cur_distance
                station = cur_station
        _LOGGER.debug("distance: %s, station: %s", distance, station)
        return station

    async def get_climatological_values_station_data(
        self, station: str, fetch_data: bool = True
    ) -> dict[str, Any]:
        """Get data from climatological values station."""
        return await self.api_call(
            f"valores/climatologicos/inventarioestaciones/estaciones/{station}",
            fetch_data,
        )

    async def get_conventional_observation_stations(
        self, fetch_data: bool = True
    ) -> dict[str, Any]:
        """Get stations available for conventional observations."""
        return await self.api_call("observacion/convencional/todas", fetch_data)

    async def get_conventional_observation_station_by_coordinates(
        self, latitude: float, longitude: float
    ) -> dict[str, Any] | None:
        """Get closest conventional observation station to coordinates."""
        stations = await self.get_conventional_observation_stations()
        search_coords = (latitude, longitude)
        station = None
        distance = API_MIN_STATION_DISTANCE_KM
        for cur_station in stations[ATTR_DATA]:
            cur_coords = (
                cur_station[AEMET_ATTR_STATION_LATITUDE],
                cur_station[AEMET_ATTR_STATION_LONGITUDE],
            )
            cur_distance = self.calc_distance(search_coords, cur_coords).km
            if cur_distance < distance:
                distance = cur_distance
                station = cur_station
        _LOGGER.debug("distance: %s, station: %s", distance, station)
        return station

    async def get_conventional_observation_station_data(
        self, station: str, fetch_data: bool = True
    ) -> dict[str, Any]:
        """Get data from conventional observation station."""
        return await self.api_call(
            f"observacion/convencional/datos/estacion/{station}", fetch_data
        )

    async def get_lightnings_map(self) -> dict[str, Any]:
        """Get map with lightning falls (last 6h)."""
        return await self.api_call("red/rayos/mapa")

    async def get_specific_forecast_town_daily(
        self, town: str, fetch_data: bool = True
    ) -> dict[str, Any]:
        """Get daily forecast for specific town (daily)."""
        return await self.api_call(
            f"prediccion/especifica/municipio/diaria/{parse_town_code(town)}",
            fetch_data,
        )

    async def get_specific_forecast_town_hourly(
        self, town: str, fetch_data: bool = True
    ) -> dict[str, Any]:
        """Get hourly forecast for specific town (hourly)."""
        return await self.api_call(
            f"prediccion/especifica/municipio/horaria/{parse_town_code(town)}",
            fetch_data,
        )

    async def get_town(self, town: str) -> dict[str, Any]:
        """Get information about specific town."""
        return await self.api_call(f"maestro/municipio/{town}")

    async def get_town_by_coordinates(
        self, latitude: float, longitude: float
    ) -> dict[str, Any] | None:
        """Get closest town to coordinates."""
        towns = await self.get_towns()
        search_coords = (latitude, longitude)
        town = None
        distance = API_MIN_TOWN_DISTANCE_KM
        for cur_town in towns[ATTR_DATA]:
            cur_coords = (
                cur_town[AEMET_ATTR_TOWN_LATITUDE_DECIMAL],
                cur_town[AEMET_ATTR_TOWN_LONGITUDE_DECIMAL],
            )
            cur_distance = self.calc_distance(search_coords, cur_coords).km
            if cur_distance < distance:
                distance = cur_distance
                town = cur_town
        _LOGGER.debug("distance: %s, town: %s", distance, town)
        return town

    async def get_towns(self) -> dict[str, Any]:
        """Get information about towns."""
        return await self.api_call("maestro/municipios")
