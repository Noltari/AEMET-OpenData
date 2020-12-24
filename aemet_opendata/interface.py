# -*- coding: utf-8 -*-
"""Client for the AEMET OpenData REST API."""

import logging
import requests
import urllib3

_LOGGER = logging.getLogger(__name__)


class AEMET:
    """Interacts with the AEMET OpenData API"""

    debug_api = False
    api_url = "https://opendata.aemet.es/opendata/api"

    def __init__(self, api_key, timeout=10, session=None):
        """Init AEMET OpenData API"""
        self.headers = {"Cache-Control": "no-cache"}
        self.params = {"api_key": api_key}
        self.session = session if session else requests.Session()
        self.timeout = timeout
        # AEMET relies on a weak HTTPS certificate
        self.verify = False
        urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL:@SECLEVEL=1"

    # Private methods
    def api_call(self, cmd):
        """Perform Rest API call"""
        if self.debug_api:
            _LOGGER.debug("api call: %s", cmd)

        url = "%s/%s" % (self.api_url, cmd)
        response = self.session.request(
            "GET",
            url,
            verify=self.verify,
            timeout=self.timeout,
            headers=self.headers,
            params=self.params,
        )

        if self.debug_api:
            _LOGGER.debug("api call: %s, response %s", cmd, response.text)

        str_response = response.text
        if str_response is None or str_response == "":
            return None

        return response.json()

    # Enable/Disable API calls debugging
    def api_debugging(self, debug_api):
        """Enable/Disable API calls debugging"""
        self.debug_api = debug_api
        return self.debug_api

    # Get specific town information
    def municipio(self, municipio):
        """Get information about specific town"""
        cmd = "maestro/municipio/%s" % municipio
        data = self.api_call(cmd)
        return data

    # Get full list of towns
    def municipios(self):
        """Get information about towns"""
        cmd = "maestro/municipios"
        data = self.api_call(cmd)
        return data
