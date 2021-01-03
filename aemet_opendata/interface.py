# -*- coding: utf-8 -*-
"""Client for the AEMET OpenData REST API."""

import logging

import requests
import urllib3

from .const import AEMET_ATTR_DATA, AEMET_ATTR_RESPONSE, API_ATTR_DATA, API_URL

_LOGGER = logging.getLogger(__name__)


class AEMET:
    """Interacts with the AEMET OpenData API"""

    def __init__(self, api_key, timeout=10, session=None, verify=True):
        """Init AEMET OpenData API"""
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
        """Perform Rest API call"""
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
        if fetch_data and API_ATTR_DATA in json_response:
            data = self.api_data(json_response[API_ATTR_DATA])
            if data:
                json_response = {
                    AEMET_ATTR_RESPONSE: json_response,
                    AEMET_ATTR_DATA: data,
                }

        return json_response

    # Fetch API data
    def api_data(self, url):
        """Fetch API data"""
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
        """Enable/Disable API calls debugging"""
        self.debug_api = debug_api
        return self.debug_api

    # Enable/Disable HTTPS verification
    def https_verify(self, verify):
        """Enable/Disable HTTPS verification"""
        self.verify = verify
        return self.verify

    # Get map of lightning strikes
    def get_lightnings_map(self):
        """Get map with lightning falls (last 6h)"""
        cmd = "red/rayos/mapa"
        data = self.api_call(cmd)
        return data

    # Get specific forecast
    def get_specific_forecast_town_daily(self, town):
        """Get daily forecast for specific town (daily)"""
        cmd = "prediccion/especifica/municipio/diaria/%s" % town
        response = self.api_call(cmd, True)
        return response

    def get_specific_forecast_town_hourly(self, town):
        """Get hourly forecast for specific town (hourly)"""
        cmd = "prediccion/especifica/municipio/horaria/%s" % town
        response = self.api_call(cmd, True)
        return response

    # Get specific town information
    def get_town(self, town):
        """Get information about specific town"""
        cmd = "maestro/municipio/%s" % town
        data = self.api_call(cmd)
        return data

    # Get full list of towns
    def get_towns(self):
        """Get information about towns"""
        cmd = "maestro/municipios"
        data = self.api_call(cmd)
        return data
