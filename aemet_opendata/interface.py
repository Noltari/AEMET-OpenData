"""Client for the AEMET OpenData REST API."""

import asyncio
from asyncio import Lock, Semaphore
import base64
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
import logging
import os
from typing import Any, Final, cast

from aiohttp import ClientError, ClientSession, ClientTimeout
from aiohttp.client_reqrep import ClientResponse
import geopy.distance
from geopy.distance import Distance

from .const import (
    AEMET_ATTR_DATA,
    AEMET_ATTR_STATE,
    AEMET_ATTR_STATION_LATITUDE,
    AEMET_ATTR_STATION_LONGITUDE,
    AEMET_ATTR_TOWN_LATITUDE_DECIMAL,
    AEMET_ATTR_TOWN_LONGITUDE_DECIMAL,
    AEMET_ATTR_WEATHER_STATION_LATITUDE,
    AEMET_ATTR_WEATHER_STATION_LONGITUDE,
    AOD_CONDITION,
    AOD_DEW_POINT,
    AOD_FEEL_TEMP,
    AOD_HUMIDITY,
    AOD_PRECIPITATION,
    AOD_PRECIPITATION_PROBABILITY,
    AOD_PRESSURE,
    AOD_RAIN,
    AOD_RAIN_PROBABILITY,
    AOD_SNOW,
    AOD_SNOW_PROBABILITY,
    AOD_STATION,
    AOD_STORM_PROBABILITY,
    AOD_TEMP,
    AOD_TIMESTAMP_UTC,
    AOD_TOWN,
    AOD_UV_INDEX,
    AOD_WEATHER,
    AOD_WIND_DIRECTION,
    AOD_WIND_SPEED,
    AOD_WIND_SPEED_MAX,
    API_CALL_DATA_TIMEOUT_DEF,
    API_CALL_FILE_EXTENSION,
    API_HDR_REQ_COUNT,
    API_MIN_STATION_DISTANCE_KM,
    API_MIN_TOWN_DISTANCE_KM,
    API_URL,
    ATTR_BYTES,
    ATTR_DATA,
    ATTR_DISTANCE,
    ATTR_RESPONSE,
    ATTR_TIMESTAMP,
    ATTR_TYPE,
    CONTENT_TYPE_IMG,
    HTTP_CALL_TIMEOUT,
    HTTP_MAX_REQUESTS,
    RAW_FORECAST_DAILY,
    RAW_FORECAST_HOURLY,
    RAW_REQ_COUNT,
    RAW_STATIONS,
    RAW_TOWNS,
)
from .exceptions import (
    AemetError,
    AemetTimeout,
    ApiError,
    AuthError,
    StationNotFound,
    TooManyRequests,
    TownNotFound,
)
from .helpers import (
    BytesEncoder,
    get_current_datetime,
    parse_api_timestamp,
    parse_station_coordinates,
    parse_town_code,
    slugify,
)
from .station import Station
from .town import Town

_LOGGER = logging.getLogger(__name__)


API_CALL_DATA_TIMEOUT: Final[dict[str, timedelta]] = {
    "maestro/municipios": timedelta(days=15),
    "prediccion/especifica/municipio/diaria": timedelta(days=3),
    "prediccion/especifica/municipio/horaria": timedelta(hours=48),
    "observacion/convencional/datos/estacion": timedelta(hours=2),
    "observacion/convencional/todas": timedelta(days=15),
    "red/radar/nacional": timedelta(hours=6),
    "red/rayos/mapa": timedelta(hours=6),
}


@dataclass
class ConnectionOptions:
    """AEMET OpenData API options for connection."""

    api_key: str
    station_data: bool = False


class AEMET:
    """Interacts with the AEMET OpenData API."""

    _api_data_dir: str | None
    _api_raw_data: dict[str, Any]
    _api_raw_data_lock: Lock
    _api_semaphore: Semaphore
    _api_timeout: ClientTimeout
    aiohttp_session: ClientSession
    coords: tuple[float, float] | None
    dist_hp: bool
    headers: dict[str, Any]
    options: ConnectionOptions
    station: Station | None
    town: Town | None

    def __init__(
        self,
        aiohttp_session: ClientSession,
        options: ConnectionOptions,
    ) -> None:
        """Init AEMET OpenData API."""
        self._api_data_dir = None
        self._api_raw_data = {
            RAW_FORECAST_DAILY: {},
            RAW_FORECAST_HOURLY: {},
            RAW_REQ_COUNT: None,
            RAW_STATIONS: {},
            RAW_TOWNS: {},
        }
        self._api_raw_data_lock = Lock()
        self._api_semaphore = Semaphore(HTTP_MAX_REQUESTS)
        self._api_timeout = ClientTimeout(total=HTTP_CALL_TIMEOUT)
        self.aiohttp_session = aiohttp_session
        self.coords = None
        self.dist_hp = False
        self.headers = {
            "Cache-Control": "no-cache",
            "api_key": options.api_key,
        }
        self.options = options
        self.station = None
        self.town = None

    def set_api_data_dir(self, data_dir: str) -> None:
        """Set API data directory."""
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self._api_data_dir = data_dir

    async def set_api_raw_data(self, key: str, subkey: str | None, data: Any) -> None:
        """Save API raw data if not empty."""
        if data is not None:
            async with self._api_raw_data_lock:
                if subkey is None:
                    self._api_raw_data[key] = data
                else:
                    self._api_raw_data[key][subkey] = data

    async def _api_call(self, cmd: str, fetch_data: bool = False) -> dict[str, Any]:
        """Perform Rest API call."""
        _LOGGER.debug("api_call: cmd=%s", cmd)

        async with self._api_semaphore:
            try:
                resp: ClientResponse = await self.aiohttp_session.request(
                    "GET",
                    f"{API_URL}/{cmd}",
                    timeout=self._api_timeout,
                    headers=self.headers,
                )
            except asyncio.TimeoutError as err:
                raise AemetTimeout(err) from err
            except ClientError as err:
                raise AemetError(err) from err

            cur_dt = get_current_datetime(replace=False)

            req_count = resp.headers.get(API_HDR_REQ_COUNT)
            if req_count is not None:
                await self.set_api_raw_data(RAW_REQ_COUNT, None, req_count)

            _LOGGER.debug(
                "api_call: cmd=%s status=%s content_type=%s",
                cmd,
                resp.status,
                resp.content_type,
            )

            if resp.status == 401:
                raise AuthError("API authentication error")
            if resp.status == 404:
                raise ApiError("API data error")
            if resp.status == 429:
                raise TooManyRequests("Too many API requests")
            if resp.status != 200:
                raise AemetError(f"API status={resp.status}")

            try:
                resp_json = await resp.json(content_type=None)
            except asyncio.TimeoutError as err:
                raise AemetTimeout(err) from err

        _LOGGER.debug("api_call: cmd=%s resp=%s", cmd, resp_json)

        if isinstance(resp_json, dict):
            if resp_json.get(AEMET_ATTR_STATE) == 404:
                raise ApiError("API data error")

        json_response = cast(dict[str, Any], resp_json)
        if fetch_data and AEMET_ATTR_DATA in json_response:
            data = await self.api_data(json_response[AEMET_ATTR_DATA])
            json_response = {
                ATTR_RESPONSE: json_response,
                ATTR_DATA: data,
            }

        json_response[ATTR_TIMESTAMP] = cur_dt.isoformat()

        return json_response

    async def api_call(self, cmd: str, fetch_data: bool = False) -> dict[str, Any]:
        """Provide data from API or file."""
        json_data: dict[str, Any] | None

        try:
            json_data = await self._api_call(cmd, fetch_data)
        except AemetError as err:
            json_data = self.api_call_load(cmd)
            if json_data is None:
                raise err
            _LOGGER.error(err)
        else:
            self.api_call_save(cmd, json_data)

        return json_data

    def api_call_load(self, cmd: str) -> dict[str, Any] | None:
        """Load API call from file."""
        json_data: dict[str, Any] | None = None

        if self._api_data_dir is None:
            return None

        file_name = slugify(cmd) + API_CALL_FILE_EXTENSION
        file_path = os.path.join(self._api_data_dir, file_name)
        if not os.path.isfile(file_path):
            return None

        data_timeout = API_CALL_DATA_TIMEOUT_DEF
        for key, val in API_CALL_DATA_TIMEOUT.items():
            if cmd.startswith(key):
                data_timeout = val
                break

        _LOGGER.info('Loading cmd=%s from "%s"...', cmd, file_name)

        with open(file_path, "r", encoding="utf-8") as file:
            file_data = file.read()
            json_data = json.loads(file_data)
            file.close()

        json_data = cast(dict[str, Any], json_data)

        file_isotime = json_data.get(ATTR_TIMESTAMP)
        if file_isotime is not None:
            file_datetime = parse_api_timestamp(file_isotime)
        else:
            file_mtime = os.path.getmtime(file_path)
            file_datetime = datetime.fromtimestamp(file_mtime, tz=timezone.utc)

        cur_datetime = get_current_datetime(replace=False)
        if cur_datetime - file_datetime > data_timeout:
            return None

        json_attr_data = json_data.get(ATTR_DATA, {})
        if isinstance(json_attr_data, dict):
            json_bytes = json_attr_data.get(ATTR_BYTES)
            if json_bytes is not None:
                json_data[ATTR_DATA][ATTR_BYTES] = base64.b64decode(json_bytes)

        return json_data

    def api_call_save(self, cmd: str, json_data: dict[str, Any]) -> None:
        """Save API call to file."""
        if self._api_data_dir is None:
            return

        file_name = slugify(cmd) + API_CALL_FILE_EXTENSION
        file_path = os.path.join(self._api_data_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(json.dumps(json_data, cls=BytesEncoder))
            file.close()

    async def api_data(self, url: str) -> Any:
        """Fetch API data."""
        _LOGGER.debug("api_data: url=%s", url)

        async with self._api_semaphore:
            try:
                resp: ClientResponse = await self.aiohttp_session.request(
                    "GET",
                    url,
                    timeout=self._api_timeout,
                )
            except asyncio.TimeoutError as err:
                raise AemetTimeout(err) from err
            except ClientError as err:
                raise AemetError(err) from err

            req_count = resp.headers.get(API_HDR_REQ_COUNT)
            if req_count is not None:
                await self.set_api_raw_data(RAW_REQ_COUNT, None, req_count)

            _LOGGER.debug(
                "api_data: url=%s status=%s content_type=%s",
                url,
                resp.status,
                resp.content_type,
            )

            if resp.status == 404:
                raise ApiError("API data error")
            if resp.status == 429:
                raise TooManyRequests("Too many API requests")
            if resp.status != 200:
                raise AemetError(f"API status={resp.status}")

            try:
                if resp.content_type.startswith(CONTENT_TYPE_IMG):
                    resp_json = {
                        ATTR_TYPE: resp.content_type,
                        ATTR_BYTES: await resp.read(),
                    }
                else:
                    resp_json = await resp.json(content_type=None)
            except asyncio.TimeoutError as err:
                raise AemetTimeout(err) from err

        _LOGGER.debug("api_data: url=%s resp=%s", url, resp_json)

        if isinstance(resp_json, dict):
            if resp_json.get(AEMET_ATTR_STATE, 200) == 404:
                raise ApiError("API data error")

        return resp_json

    def raw_data(self) -> dict[str, Any]:
        """Return raw AEMET OpenData API data."""
        return self._api_raw_data

    def data(self) -> dict[str, Any]:
        """Return AEMET OpenData data."""
        data: dict[str, Any] = {}

        if self.station is not None:
            data[AOD_STATION] = self.station.data()

        if self.town is not None:
            data[AOD_TOWN] = self.town.data()

        weather = self.weather()
        if weather is not None:
            data[AOD_WEATHER] = weather

        data[AOD_TIMESTAMP_UTC] = get_current_datetime().isoformat()

        return data

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
    ) -> dict[str, Any]:
        """Get closest climatological values station to coordinates."""
        station: dict[str, Any] | None = None
        stations = await self.get_climatological_values_stations()
        search_coords = (latitude, longitude)
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
        if station is None:
            raise StationNotFound(f"No stations found for [{latitude}, {longitude}]")
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
    ) -> dict[str, Any]:
        """Get closest conventional observation station to coordinates."""
        station: dict[str, Any] | None = None
        stations = await self.get_conventional_observation_stations()
        search_coords = (latitude, longitude)
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
        if station is None:
            raise StationNotFound(f"No stations found for [{latitude}, {longitude}]")
        _LOGGER.debug("distance: %s, station: %s", distance, station)
        station[ATTR_DISTANCE] = distance
        return station

    async def get_conventional_observation_station_data(
        self, station: str, fetch_data: bool = True
    ) -> dict[str, Any]:
        """Get data from conventional observation station."""
        res = await self.api_call(
            f"observacion/convencional/datos/estacion/{station}", fetch_data
        )
        await self.set_api_raw_data(RAW_STATIONS, station, res)
        return res

    async def get_lightnings_map(self, fetch_data: bool = True) -> dict[str, Any]:
        """Get map with lightning falls (last 6h)."""
        return await self.api_call("red/rayos/mapa", fetch_data)

    async def get_radar_map(
        self, region: str | None = None, fetch_data: bool = True
    ) -> dict[str, Any]:
        """Get weather radar map."""
        if region is not None:
            api_cmd = f"red/radar/regional/{region}"
        else:
            api_cmd = "red/radar/nacional"
        return await self.api_call(api_cmd, fetch_data)

    async def get_specific_forecast_town_daily(
        self, town: str, fetch_data: bool = True
    ) -> dict[str, Any]:
        """Get daily forecast for specific town (daily)."""
        res = await self.api_call(
            f"prediccion/especifica/municipio/diaria/{parse_town_code(town)}",
            fetch_data,
        )
        await self.set_api_raw_data(RAW_FORECAST_DAILY, town, res)
        return res

    async def get_specific_forecast_town_hourly(
        self, town: str, fetch_data: bool = True
    ) -> dict[str, Any]:
        """Get hourly forecast for specific town (hourly)."""
        res = await self.api_call(
            f"prediccion/especifica/municipio/horaria/{parse_town_code(town)}",
            fetch_data,
        )
        await self.set_api_raw_data(RAW_FORECAST_HOURLY, town, res)
        return res

    async def get_town(self, town: str) -> dict[str, Any]:
        """Get information about specific town."""
        res = await self.api_call(f"maestro/municipio/{town}")
        await self.set_api_raw_data(RAW_TOWNS, town, res)
        return res

    async def get_town_by_coordinates(
        self, latitude: float, longitude: float
    ) -> dict[str, Any]:
        """Get closest town to coordinates."""
        town: dict[str, Any] | None = None
        towns = await self.get_towns()
        search_coords = (latitude, longitude)
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
        if town is None:
            raise TownNotFound(f"No towns found for [{latitude}, {longitude}]")
        _LOGGER.debug("distance: %s, town: %s", distance, town)
        town[ATTR_DISTANCE] = distance
        return town

    async def get_towns(self, fetch_data: bool = True) -> dict[str, Any]:
        """Get information about towns."""
        return await self.api_call("maestro/municipios", fetch_data)

    async def select_coordinates(self, latitude: float, longitude: float) -> None:
        """Select town and station based on provided coordinates."""
        coords = (latitude, longitude)

        if self.options.station_data:
            try:
                station_data = (
                    await self.get_conventional_observation_station_by_coordinates(
                        latitude,
                        longitude,
                    )
                )
            except StationNotFound as err:
                _LOGGER.error(err)
                station_data = None
        else:
            station_data = None

        town_data = await self.get_town_by_coordinates(latitude, longitude)

        self.coords = coords
        if station_data is not None:
            self.station = Station(station_data)
        self.town = Town(town_data)

    async def update_daily(self) -> None:
        """Update AEMET OpenData town daily forecast."""
        if self.town is not None:
            town_id = self.town.get_id()
            daily = await self.get_specific_forecast_town_daily(town_id)
            self.town.update_daily(daily)

    async def update_hourly(self) -> None:
        """Update AEMET OpenData town hourly forecast."""
        if self.town is not None:
            town_id = self.town.get_id()
            hourly = await self.get_specific_forecast_town_hourly(town_id)
            self.town.update_hourly(hourly)

    async def update_station(self) -> None:
        """Update AEMET OpenData station."""
        if self.station is not None:
            station_id = self.station.get_id()
            station = await self.get_conventional_observation_station_data(station_id)
            self.station.update_samples(station)

    async def update(self) -> None:
        """Update all AEMET OpenData data."""
        tasks = [
            asyncio.create_task(self.update_daily()),
            asyncio.create_task(self.update_hourly()),
            asyncio.create_task(self.update_station()),
        ]
        await asyncio.gather(*tasks)

    def weather(self) -> dict[str, Any] | None:
        """Update AEMET OpenData town daily forecast."""
        daily: dict[str, Any]
        hourly: dict[str, Any]
        station: dict[str, Any]

        if self.station is not None and not self.station.get_outdated():
            station = self.station.weather()
        else:
            station = {}

        if self.town is not None:
            daily = self.town.weather_daily()
            hourly = self.town.weather_hourly()
        else:
            daily = {}
            hourly = {}

        condition = hourly.get(AOD_CONDITION) or daily.get(AOD_CONDITION)
        dew_point = station.get(AOD_DEW_POINT)
        feel_temp = hourly.get(AOD_FEEL_TEMP)
        humidity = station.get(AOD_HUMIDITY)
        if humidity is None:
            humidity = hourly.get(AOD_HUMIDITY)
        pressure = station.get(AOD_PRESSURE)
        precipitation = station.get(AOD_PRECIPITATION)
        if precipitation is None:
            precipitation = hourly.get(AOD_PRECIPITATION)
        precipitation_prob = hourly.get(AOD_PRECIPITATION_PROBABILITY)
        if precipitation_prob is None:
            precipitation_prob = daily.get(AOD_PRECIPITATION_PROBABILITY)
        rain = station.get(AOD_PRECIPITATION)
        if rain is None:
            rain = hourly.get(AOD_RAIN)
        rain_prob = hourly.get(AOD_RAIN_PROBABILITY)
        snow = hourly.get(AOD_SNOW)
        snow_prob = hourly.get(AOD_SNOW_PROBABILITY)
        storm_prob = hourly.get(AOD_STORM_PROBABILITY)
        temp = station.get(AOD_TEMP)
        if temp is None:
            temp = hourly.get(AOD_TEMP)
        uv_index = daily.get(AOD_UV_INDEX)
        wind_direction = (
            station.get(AOD_WIND_DIRECTION)
            or hourly.get(AOD_WIND_DIRECTION)
            or daily.get(AOD_WIND_DIRECTION)
        )
        wind_speed = (
            station.get(AOD_WIND_SPEED)
            or hourly.get(AOD_WIND_SPEED)
            or daily.get(AOD_WIND_SPEED)
        )
        wind_speed_max = station.get(AOD_WIND_SPEED_MAX) or hourly.get(
            AOD_WIND_SPEED_MAX
        )

        weather: dict[str, Any] = {
            AOD_CONDITION: condition,
            AOD_DEW_POINT: dew_point,
            AOD_HUMIDITY: humidity,
            AOD_FEEL_TEMP: feel_temp,
            AOD_PRECIPITATION: precipitation,
            AOD_PRECIPITATION_PROBABILITY: precipitation_prob,
            AOD_PRESSURE: pressure,
            AOD_RAIN: rain,
            AOD_RAIN_PROBABILITY: rain_prob,
            AOD_SNOW: snow,
            AOD_SNOW_PROBABILITY: snow_prob,
            AOD_STORM_PROBABILITY: storm_prob,
            AOD_TEMP: temp,
            AOD_UV_INDEX: uv_index,
            AOD_WIND_DIRECTION: wind_direction,
            AOD_WIND_SPEED: wind_speed,
            AOD_WIND_SPEED_MAX: wind_speed_max,
        }

        return weather
