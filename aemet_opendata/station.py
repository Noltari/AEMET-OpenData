"""AEMET OpenData Station."""

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .const import (
    AEMET_ATTR_IDEMA,
    AEMET_ATTR_STATION_ALTITUDE,
    AEMET_ATTR_STATION_DATE,
    AEMET_ATTR_STATION_DEWPOINT,
    AEMET_ATTR_STATION_HUMIDITY,
    AEMET_ATTR_STATION_LATITUDE,
    AEMET_ATTR_STATION_LOCATION,
    AEMET_ATTR_STATION_LONGITUDE,
    AEMET_ATTR_STATION_PRECIPITATION,
    AEMET_ATTR_STATION_PRESSURE,
    AEMET_ATTR_STATION_PRESSURE_SEA,
    AEMET_ATTR_STATION_TEMPERATURE,
    AEMET_ATTR_STATION_TEMPERATURE_MAX,
    AEMET_ATTR_STATION_TEMPERATURE_MIN,
    AEMET_ATTR_STATION_WIND_DIRECTION,
    AEMET_ATTR_STATION_WIND_SPEED,
    AEMET_ATTR_STATION_WIND_SPEED_MAX,
    AOD_ALTITUDE,
    AOD_COORDS,
    AOD_DATETIME,
    AOD_DEW_POINT,
    AOD_DISTANCE,
    AOD_HUMIDITY,
    AOD_ID,
    AOD_NAME,
    AOD_OUTDATED,
    AOD_PRECIPITATION,
    AOD_PRESSURE,
    AOD_TEMP,
    AOD_TEMP_MAX,
    AOD_TEMP_MIN,
    AOD_TIMESTAMP_UTC,
    AOD_TIMEZONE,
    AOD_WIND_DIRECTION,
    AOD_WIND_SPEED,
    AOD_WIND_SPEED_MAX,
    ATTR_DATA,
    ATTR_DISTANCE,
    STATION_MAX_DELTA,
)
from .helpers import get_current_datetime, parse_api_timestamp, timezone_from_coords


class Station:
    """AEMET OpenData Station."""

    altitude: float
    coords: tuple[float, float]
    _datetime: datetime
    distance: float
    dew_point: float | None = None
    humidity: float | None = None
    id: str
    name: str
    precipitation: float | None = None
    pressure: float | None = None
    temp: float | None = None
    temp_max: float | None = None
    temp_min: float | None = None
    wind_direction: float | None = None
    wind_speed: float | None = None
    wind_speed_max: float | None = None
    zoneinfo: ZoneInfo

    def __init__(self, data: dict[str, Any]) -> None:
        """Init AEMET OpenData Station."""

        self.altitude = float(data[AEMET_ATTR_STATION_ALTITUDE])
        self.coords = (
            float(data[AEMET_ATTR_STATION_LATITUDE]),
            float(data[AEMET_ATTR_STATION_LONGITUDE]),
        )
        self.distance = float(data[ATTR_DISTANCE])
        self.id = str(data[AEMET_ATTR_IDEMA])
        self.name = str(data[AEMET_ATTR_STATION_LOCATION])
        self.zoneinfo = timezone_from_coords(self.coords)

        self.update_sample(data)

    def get_altitude(self) -> float:
        """Return Station altitude."""
        return self.altitude

    def get_coords(self) -> tuple[float, float]:
        """Return Station coordinates."""
        return self.coords

    def get_datetime(self) -> datetime:
        """Return Station datetime of data."""
        return self._datetime

    def get_distance(self) -> float:
        """Return Station distance from selected coordinates."""
        return round(self.distance, 3)

    def get_dew_point(self) -> float | None:
        """Return Station dew point."""
        return self.dew_point

    def get_humidity(self) -> float | None:
        """Return Station humidity."""
        return self.humidity

    def get_id(self) -> str:
        """Return Station ID."""
        return self.id

    def get_name(self) -> str | None:
        """Return Station name."""
        return self.name

    def get_outdated(self) -> bool:
        """Return Station data outdated."""
        cur_dt = get_current_datetime()
        return cur_dt > self.get_datetime() + STATION_MAX_DELTA

    def get_precipitation(self) -> float | None:
        """Return Station precipitation."""
        return self.precipitation

    def get_pressure(self) -> float | None:
        """Return Station pressure."""
        return self.pressure

    def get_temp(self) -> float | None:
        """Return Station temperature."""
        return self.temp

    def get_temp_max(self) -> float | None:
        """Return Station maximum temperature."""
        return self.temp_max

    def get_temp_min(self) -> float | None:
        """Return Station minimum temperature."""
        return self.temp_min

    def get_timestamp_utc(self) -> str:
        """Return Station UTC timestamp."""
        return self._datetime.isoformat()

    def get_timezone(self) -> ZoneInfo:
        """Return Station timezone."""
        return self.zoneinfo

    def get_wind_direction(self) -> float | None:
        """Return Station wind direction."""
        return self.wind_direction

    def get_wind_speed(self) -> float | None:
        """Return Station wind speed."""
        return self.wind_speed

    def get_wind_speed_max(self) -> float | None:
        """Return Station maximum wind speed."""
        return self.wind_speed_max

    def update_sample(self, data: dict[str, Any]) -> None:
        """Update Station data from sample."""
        station_dt = parse_api_timestamp(data[AEMET_ATTR_STATION_DATE])

        self._datetime = station_dt.astimezone(self.get_timezone())

        if AEMET_ATTR_STATION_DEWPOINT in data:
            self.dew_point = float(data[AEMET_ATTR_STATION_DEWPOINT])

        if AEMET_ATTR_STATION_HUMIDITY in data:
            self.humidity = float(data[AEMET_ATTR_STATION_HUMIDITY])

        if AEMET_ATTR_STATION_PRECIPITATION in data:
            self.precipitation = float(data[AEMET_ATTR_STATION_PRECIPITATION])

        if AEMET_ATTR_STATION_PRESSURE_SEA in data:
            self.pressure = float(data[AEMET_ATTR_STATION_PRESSURE_SEA])
        elif AEMET_ATTR_STATION_PRESSURE in data:
            self.pressure = float(data[AEMET_ATTR_STATION_PRESSURE])

        if AEMET_ATTR_STATION_TEMPERATURE in data:
            self.temp = float(data[AEMET_ATTR_STATION_TEMPERATURE])

        if AEMET_ATTR_STATION_TEMPERATURE_MAX in data:
            self.temp_max = float(data[AEMET_ATTR_STATION_TEMPERATURE_MAX])

        if AEMET_ATTR_STATION_TEMPERATURE_MIN in data:
            self.temp_min = float(data[AEMET_ATTR_STATION_TEMPERATURE_MIN])

        if AEMET_ATTR_STATION_WIND_DIRECTION in data:
            self.wind_direction = float(data[AEMET_ATTR_STATION_WIND_DIRECTION])

        if AEMET_ATTR_STATION_WIND_SPEED in data:
            self.wind_speed = float(data[AEMET_ATTR_STATION_WIND_SPEED])

        if AEMET_ATTR_STATION_WIND_SPEED_MAX in data:
            self.wind_speed_max = float(data[AEMET_ATTR_STATION_WIND_SPEED_MAX])

    def update_samples(self, samples: dict[str, Any]) -> None:
        """Update Station data from samples."""
        latest: dict[str, Any]
        latest_dt: datetime | None = None
        for sample in samples[ATTR_DATA]:
            dt = parse_api_timestamp(sample[AEMET_ATTR_STATION_DATE])
            if latest_dt is None or dt > latest_dt:
                latest = sample
                latest_dt = dt
        if (
            latest_dt is not None
            and self.get_datetime() < latest_dt <= get_current_datetime()
        ):
            self.update_sample(latest)

    def data(self) -> dict[str, Any]:
        """Return station data."""
        data: dict[str, Any] = {
            AOD_ALTITUDE: self.get_altitude(),
            AOD_COORDS: self.get_coords(),
            AOD_DATETIME: self.get_datetime(),
            AOD_DISTANCE: self.get_distance(),
            AOD_ID: self.get_id(),
            AOD_NAME: self.get_name(),
            AOD_OUTDATED: self.get_outdated(),
            AOD_TIMESTAMP_UTC: self.get_timestamp_utc(),
            AOD_TIMEZONE: self.get_timezone(),
        }

        dew_point = self.get_dew_point()
        if dew_point is not None:
            data[AOD_DEW_POINT] = dew_point

        humidity = self.get_humidity()
        if humidity is not None:
            data[AOD_HUMIDITY] = humidity

        precipitation = self.get_precipitation()
        if precipitation is not None:
            data[AOD_PRECIPITATION] = precipitation

        pressure = self.get_pressure()
        if pressure is not None:
            data[AOD_PRESSURE] = pressure

        temp = self.get_temp()
        if temp is not None:
            data[AOD_TEMP] = temp

        temp_max = self.get_temp_max()
        if temp_max is not None:
            data[AOD_TEMP_MAX] = temp_max

        temp_min = self.get_temp_min()
        if temp_min is not None:
            data[AOD_TEMP_MIN] = temp_min

        wind_direction = self.get_wind_direction()
        if wind_direction is not None:
            data[AOD_WIND_DIRECTION] = wind_direction

        wind_speed = self.get_wind_speed()
        if wind_speed is not None:
            data[AOD_WIND_SPEED] = wind_speed

        wind_speed_max = self.get_wind_speed_max()
        if wind_speed_max is not None:
            data[AOD_WIND_SPEED_MAX] = wind_speed_max

        return data

    def weather(self) -> dict[str, Any]:
        """Return Station weather data."""
        weather: dict[str, Any] = {}

        dew_point = self.get_dew_point()
        if dew_point is not None:
            weather[AOD_DEW_POINT] = dew_point

        humidity = self.get_humidity()
        if humidity is not None:
            weather[AOD_HUMIDITY] = humidity

        precipitation = self.get_precipitation()
        if precipitation is not None:
            weather[AOD_PRECIPITATION] = precipitation

        pressure = self.get_pressure()
        if pressure is not None:
            weather[AOD_PRESSURE] = pressure

        temp = self.get_temp()
        if temp is not None:
            weather[AOD_TEMP] = temp

        wind_direction = self.get_wind_direction()
        if wind_direction is not None:
            weather[AOD_WIND_DIRECTION] = wind_direction

        wind_speed = self.get_wind_speed()
        if wind_speed is not None:
            weather[AOD_WIND_SPEED] = wind_speed

        wind_speed_max = self.get_wind_speed_max()
        if wind_speed_max is not None:
            weather[AOD_WIND_SPEED_MAX] = wind_speed_max

        return weather
