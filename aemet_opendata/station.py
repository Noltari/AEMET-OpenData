"""AEMET OpenData Station."""

from typing import Any

from .const import (
    AEMET_ATTR_IDEMA,
    AEMET_ATTR_STATION_ALTITUDE,
    AEMET_ATTR_STATION_DATE,
    AEMET_ATTR_STATION_HUMIDITY,
    AEMET_ATTR_STATION_LATITUDE,
    AEMET_ATTR_STATION_LOCATION,
    AEMET_ATTR_STATION_LONGITUDE,
    AEMET_ATTR_STATION_PRESSURE,
    AEMET_ATTR_STATION_PRESSURE_SEA,
    AEMET_ATTR_STATION_TEMPERATURE,
    AEMET_ATTR_STATION_TEMPERATURE_MAX,
    AEMET_ATTR_STATION_TEMPERATURE_MIN,
    AOD_ALTITUDE,
    AOD_COORDS,
    AOD_DATA,
    AOD_HUMIDITY,
    AOD_ID,
    AOD_NAME,
    AOD_PRESSURE,
    AOD_TEMP,
    AOD_TEMP_MAX,
    AOD_TEMP_MIN,
    AOD_TIMESTAMP,
    ATTR_DATA,
    RAW_DATA,
    RAW_INFO,
)


class StationData:
    """AEMET OpenData StationData."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Init AEMET OpenData StationData."""
        self.humidity = float(data[AEMET_ATTR_STATION_HUMIDITY])
        if AEMET_ATTR_STATION_PRESSURE_SEA in data:
            self.pressure = float(data[AEMET_ATTR_STATION_PRESSURE_SEA])
        else:
            self.pressure = float(data[AEMET_ATTR_STATION_PRESSURE])
        self.temp = float(data[AEMET_ATTR_STATION_TEMPERATURE])
        self.temp_max = float(data[AEMET_ATTR_STATION_TEMPERATURE_MAX])
        self.temp_min = float(data[AEMET_ATTR_STATION_TEMPERATURE_MIN])
        self.timestamp = str(data[AEMET_ATTR_STATION_DATE]) + "Z"

    def get_humidity(self) -> float:
        """Return StationData humidity."""
        return self.humidity

    def get_pressure(self) -> float:
        """Return StationData pressure."""
        return self.pressure

    def get_temp(self) -> float:
        """Return StationData temperature."""
        return self.temp

    def get_temp_max(self) -> float:
        """Return StationData maximum temperature."""
        return self.temp_max

    def get_temp_min(self) -> float:
        """Return StationData minimum temperature."""
        return self.temp_min

    def get_timestamp(self) -> str:
        """Return StationData timestamp."""
        return self.timestamp

    def data(self) -> dict[str, Any]:
        """Return StationData data."""
        data: dict[str, Any] = {
            AOD_HUMIDITY: self.get_humidity(),
            AOD_PRESSURE: self.get_pressure(),
            AOD_TEMP: self.get_temp(),
            AOD_TEMP_MAX: self.get_temp_max(),
            AOD_TEMP_MIN: self.get_temp_min(),
            AOD_TIMESTAMP: self.get_timestamp(),
        }

        return data


class Station:
    """AEMET OpenData Station."""

    def __init__(self, data: dict[str, Any]) -> None:
        """Init AEMET OpenData Station."""
        self._api_raw_data = {
            RAW_INFO: data,
        }
        self.altitude = float(data[AEMET_ATTR_STATION_ALTITUDE])
        self.coords = (
            float(data[AEMET_ATTR_STATION_LATITUDE]),
            float(data[AEMET_ATTR_STATION_LONGITUDE]),
        )
        self.entries: list[StationData] = []
        self.id = str(data[AEMET_ATTR_IDEMA])
        self.name = str(data[AEMET_ATTR_STATION_LOCATION])

    def get_altitude(self) -> float:
        """Return Station altitude."""
        return self.altitude

    def get_coords(self) -> tuple[float, float]:
        """Return Station coordinates."""
        return self.coords

    def get_id(self) -> str:
        """Return Station ID."""
        return self.id

    def get_name(self) -> str:
        """Return Station name."""
        return self.name

    def update(self, data: dict[str, Any]) -> None:
        """Update Station data."""
        entries = []

        for cur_data in data[ATTR_DATA]:
            entry = StationData(cur_data)
            entries += [entry]

        self._api_raw_data[RAW_DATA] = data
        self.entries = entries

    def raw_data(self) -> dict[str, Any]:
        """Return raw Station data."""
        return self._api_raw_data

    def data(self) -> dict[str, Any]:
        """Return station data."""
        data: dict[str, Any] = {
            AOD_ALTITUDE: self.get_altitude(),
            AOD_COORDS: self.get_coords(),
            AOD_ID: self.get_id(),
            AOD_NAME: self.get_name(),
            AOD_DATA: [],
        }

        for entry in self.entries:
            data[AOD_DATA] += [entry.data()]

        return data
