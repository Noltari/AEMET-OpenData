# -*- coding: utf-8 -*-
"""Client for the AEMET OpenData REST API."""

import logging

import geopy.distance
import requests
import urllib3

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
    API_URL,
    ATTR_DATA,
    ATTR_RESPONSE,
)
from .helpers import parse_station_coordinates, parse_town_code

_LOGGER = logging.getLogger(__name__)


class AEMET:
    """Interacts with the AEMET OpenData API."""

    def __init__(self, api_key, timeout=10, session=None, verify=True):
        """Init AEMET OpenData API."""
        self.debug_api = False
        self.headers = {"Cache-Control": "no-cache"}
        self.params = {"api_key": api_key}
        self.session = session if session else requests.Session()
        self.timeout = timeout
        self.verify = verify
        # AEMET relies on a weak HTTPS certificate
        urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL:@SECLEVEL=1"

    # Perform API call
    def api_call(self, cmd, fetch_data=False):
        """Perform Rest API call."""
        if self.debug_api:
            _LOGGER.debug("api call: %s", cmd)

        url = "%s/%s" % (API_URL, cmd)
        response = self.session.request(
            "GET",
            url,
            verify=self.verify,
            timeout=self.timeout,
            headers=self.headers,
            params=self.params,
        )

        if self.debug_api:
            _LOGGER.debug(
                "api call: %s, status: %s, response %s",
                cmd,
                response.status_code,
                response.text,
            )

        if response.status_code != 200:
            return None

        str_response = response.text
        if str_response is None or str_response == "":
            return None

        json_response = response.json()
        if fetch_data and AEMET_ATTR_DATA in json_response:
            data = self.api_data(json_response[AEMET_ATTR_DATA])
            if data:
                json_response = {
                    ATTR_RESPONSE: json_response,
                    ATTR_DATA: data,
                }

        return json_response

    # Fetch API data
    def api_data(self, url):
        """Fetch API data."""
        response = self.session.request(
            "GET",
            url,
            verify=self.verify,
            timeout=self.timeout,
        )

        if self.debug_api:
            _LOGGER.debug(
                "api data: %s, status: %s, response %s",
                url,
                response.status_code,
                response.text,
            )

        if response.status_code != 200:
            return None

        str_response = response.text
        if str_response is None or str_response == "":
            return None

        return response.json()

    # Enable/Disable API calls debugging
    def api_debugging(self, debug_api):
        """Enable/Disable API calls debugging."""
        self.debug_api = debug_api
        return self.debug_api

    # Enable/Disable HTTPS verification
    def https_verify(self, verify):
        """Enable/Disable HTTPS verification."""
        self.verify = verify
        return self.verify

    # Get climatological values
    def get_climatological_values_stations(self, fetch_data=True):
        """Get stations available for climatological values."""
        cmd = "valores/climatologicos/inventarioestaciones/todasestaciones"
        response = self.api_call(cmd, fetch_data)
        return response

    # Get climatological values station by coordinates
    def get_climatological_values_station_by_coordinates(self, latitude, longitude):
        """Get closest climatological values station to coordinates."""
        stations = self.get_climatological_values_stations()
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
            cur_distance = geopy.distance.distance(search_coords, cur_coords).km
            if cur_distance < distance:
                distance = cur_distance
                station = cur_station
        if self.debug_api:
            _LOGGER.debug("distance: %s, station: %s", distance, station)
        return station

    # Get climatological values station data
    def get_climatological_values_station_data(self, station, fetch_data=True):
        """Get data from climatological values station."""
        cmd = "valores/climatologicos/inventarioestaciones/estaciones/%s" % station
        response = self.api_call(cmd, fetch_data)
        return response

    # Get conventional observation stations
    def get_conventional_observation_stations(self, fetch_data=True):
        """Get stations available for conventional observations."""
        cmd = "observacion/convencional/todas"
        response = self.api_call(cmd, fetch_data)
        return response

    # Get conventional observation station by coordinates
    def get_conventional_observation_station_by_coordinates(self, latitude, longitude):
        """Get closest conventional observation station to coordinates."""
        stations = self.get_conventional_observation_stations()
        search_coords = (latitude, longitude)
        station = None
        distance = API_MIN_STATION_DISTANCE_KM
        for cur_station in stations[ATTR_DATA]:
            cur_coords = (
                cur_station[AEMET_ATTR_STATION_LATITUDE],
                cur_station[AEMET_ATTR_STATION_LONGITUDE],
            )
            cur_distance = geopy.distance.distance(search_coords, cur_coords).km
            if cur_distance < distance:
                distance = cur_distance
                station = cur_station
        if self.debug_api:
            _LOGGER.debug("distance: %s, station: %s", distance, station)
        return station

    # Get conventional observation station data
    def get_conventional_observation_station_data(self, station, fetch_data=True):
        """Get data from conventional observation station."""
        cmd = "observacion/convencional/datos/estacion/%s" % station
        response = self.api_call(cmd, fetch_data)
        return response

    # Get map of lightning strikes
    def get_lightnings_map(self):
        """Get map with lightning falls (last 6h)."""
        cmd = "red/rayos/mapa"
        data = self.api_call(cmd)
        return data

    # Get specific forecast
    def get_specific_forecast_town_daily(self, town, fetch_data=True):
        """Get daily forecast for specific town (daily)."""
        cmd = "prediccion/especifica/municipio/diaria/%s" % parse_town_code(town)
        response = self.api_call(cmd, fetch_data)
        return response

    def get_specific_forecast_town_hourly(self, town, fetch_data=True):
        """Get hourly forecast for specific town (hourly)."""
        cmd = "prediccion/especifica/municipio/horaria/%s" % parse_town_code(town)
        response = self.api_call(cmd, fetch_data)
        return response

    # Get specific town information
    def get_town(self, town):
        """Get information about specific town."""
        cmd = "maestro/municipio/%s" % town
        data = self.api_call(cmd)
        return data

    # Get town by coordinates
    def get_town_by_coordinates(self, latitude, longitude):
        """Get closest town to coordinates."""
        towns = self.get_towns()
        search_coords = (latitude, longitude)
        town = None
        distance = API_MIN_TOWN_DISTANCE_KM
        for cur_town in towns:
            cur_coords = (
                cur_town[AEMET_ATTR_TOWN_LATITUDE_DECIMAL],
                cur_town[AEMET_ATTR_TOWN_LONGITUDE_DECIMAL],
            )
            cur_distance = geopy.distance.distance(search_coords, cur_coords).km
            if cur_distance < distance:
                distance = cur_distance
                town = cur_town
        if self.debug_api:
            _LOGGER.debug("distance: %s, town: %s", distance, town)
        return town

    # Get full list of towns
    def get_towns(self):
        """Get information about towns."""
        cmd = "maestro/municipios"
        data = self.api_call(cmd)
        return data
