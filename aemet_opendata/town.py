"""AEMET OpenData Town."""

from typing import Any

from .const import (
    AEMET_ATTR_ID,
    AEMET_ATTR_NAME,
    AEMET_ATTR_TOWN_ALTITUDE,
    AEMET_ATTR_TOWN_LATITUDE_DECIMAL,
    AEMET_ATTR_TOWN_LONGITUDE_DECIMAL,
    AOD_ALTITUDE,
    AOD_COORDS,
    AOD_DATA,
    AOD_ID,
    AOD_NAME,
    RAW_FORECAST_DAILY,
    RAW_FORECAST_HOURLY,
    RAW_INFO,
)


class Town:
    """AEMET OpenData Town."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Init AEMET OpenData Town."""
        self._api_raw_data = {
            RAW_INFO: data,
        }
        self.altitude = int(data[AEMET_ATTR_TOWN_ALTITUDE])
        self.coords = (
            float(data[AEMET_ATTR_TOWN_LATITUDE_DECIMAL]),
            float(data[AEMET_ATTR_TOWN_LONGITUDE_DECIMAL]),
        )
        self.daily: list[Any] = []
        self.hourly: list[Any] = []
        self.id = str(data[AEMET_ATTR_ID])
        self.name = str(data[AEMET_ATTR_NAME])

    def get_altitude(self) -> int:
        """Return Town altitude."""
        return self.altitude

    def get_coords(self) -> tuple[float, float]:
        """Return Town coordinates."""
        return self.coords

    def get_id(self) -> str:
        """Return Town ID."""
        return self.id

    def get_name(self) -> str:
        """Return Town name."""
        return self.name

    def update_daily(self, data: dict[str, Any]) -> None:
        """Update Town daily forecast."""
        daily: list[Any] = []

        self._api_raw_data[RAW_FORECAST_DAILY] = data
        self.daily = daily

    def update_hourly(self, data: dict[str, Any]) -> None:
        """Update Town hourly forecast."""
        hourly: list[Any] = []

        self._api_raw_data[RAW_FORECAST_HOURLY] = data
        self.hourly = hourly

    def raw_data(self) -> dict[str, Any]:
        """Return raw Town data."""
        return self._api_raw_data

    def data(self) -> dict[str, Any]:
        """Return Town data."""
        data: dict[str, Any] = {
            AOD_ALTITUDE: self.get_altitude(),
            AOD_COORDS: self.get_coords(),
            AOD_ID: self.get_id(),
            AOD_NAME: self.get_name(),
            AOD_DATA: [],
        }

        return data
