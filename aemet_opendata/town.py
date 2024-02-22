"""AEMET OpenData Town."""

from datetime import datetime, timezone
import logging
from typing import Any
from zoneinfo import ZoneInfo

from .const import (
    AEMET_ATTR_DATE,
    AEMET_ATTR_DAY,
    AEMET_ATTR_ELABORATED,
    AEMET_ATTR_FORECAST,
    AEMET_ATTR_ID,
    AEMET_ATTR_NAME,
    AEMET_ATTR_TOWN_ALTITUDE,
    AEMET_ATTR_TOWN_LATITUDE_DECIMAL,
    AEMET_ATTR_TOWN_LONGITUDE_DECIMAL,
    AEMET_ATTR_TOWN_RESIDENTS,
    AOD_ALTITUDE,
    AOD_CONDITION,
    AOD_COORDS,
    AOD_DISTANCE,
    AOD_FEEL_TEMP,
    AOD_FORECAST,
    AOD_FORECAST_CURRENT,
    AOD_FORECAST_DAILY,
    AOD_FORECAST_HOURLY,
    AOD_HUMIDITY,
    AOD_ID,
    AOD_NAME,
    AOD_PRECIPITATION,
    AOD_PRECIPITATION_PROBABILITY,
    AOD_RAIN,
    AOD_RAIN_PROBABILITY,
    AOD_RESIDENTS,
    AOD_SNOW,
    AOD_SNOW_PROBABILITY,
    AOD_STORM_PROBABILITY,
    AOD_TEMP,
    AOD_TIMESTAMP_LOCAL,
    AOD_TIMESTAMP_UTC,
    AOD_TIMEZONE,
    AOD_UV_INDEX,
    AOD_WIND_DIRECTION,
    AOD_WIND_SPEED,
    AOD_WIND_SPEED_MAX,
    ATTR_DATA,
    ATTR_DISTANCE,
)
from .forecast import DailyForecastValue, HourlyForecastValue
from .helpers import get_current_datetime, parse_api_timestamp, timezone_from_coords

_LOGGER = logging.getLogger(__name__)


class DailyForecast:
    """AEMET OpenData Town Daily Forecast."""

    _datetime: datetime
    forecast: list[DailyForecastValue]
    zoneinfo: ZoneInfo

    def __init__(self, data: dict[str, Any], zoneinfo: ZoneInfo) -> None:
        """Init AEMET OpenData Town Daily Forecast."""
        self._datetime = parse_api_timestamp(data[AEMET_ATTR_ELABORATED])
        self.forecast: list[DailyForecastValue] = []
        self.zoneinfo = zoneinfo

        cur_dt = get_current_datetime(zoneinfo)
        cur_day = cur_dt.date()

        for day_data in data[AEMET_ATTR_FORECAST][AEMET_ATTR_DAY]:
            day = parse_api_timestamp(day_data[AEMET_ATTR_DATE], zoneinfo)
            if cur_day <= day.date():
                try:
                    self.forecast += [DailyForecastValue(day_data, day)]
                except ValueError as err:
                    _LOGGER.debug(err)

    def get_current_forecast(self) -> DailyForecastValue | None:
        """Return Town current daily forecast."""
        cur_date = get_current_datetime(self.get_timezone()).date()
        for forecast in self.forecast:
            forecast_date = forecast.get_datetime().date()
            if cur_date == forecast_date:
                return forecast
        return None

    def get_timestamp_local(self) -> str:
        """Return Town daily forecast timestamp."""
        return self._datetime.isoformat()

    def get_timestamp_utc(self) -> str:
        """Return Town daily forecast timestamp."""
        return self._datetime.astimezone(timezone.utc).isoformat()

    def get_timezone(self) -> ZoneInfo:
        """Return Town daily forecast timezone."""
        return self.zoneinfo

    def data(self) -> dict[str, Any]:
        """Return Town daily forecast data."""
        data: dict[str, Any] = {
            AOD_FORECAST: [],
            AOD_TIMESTAMP_LOCAL: self.get_timestamp_local(),
            AOD_TIMESTAMP_UTC: self.get_timestamp_utc(),
            AOD_TIMEZONE: self.get_timezone(),
        }

        cur_date = get_current_datetime(self.get_timezone()).date()
        for forecast in self.forecast:
            forecast_date = forecast.get_datetime().date()
            if cur_date <= forecast_date:
                data[AOD_FORECAST] += [forecast.data()]

        cur_forecast = self.get_current_forecast()
        if cur_forecast is not None:
            data[AOD_FORECAST_CURRENT] = cur_forecast.data()

        return data

    def weather(self) -> dict[str, Any]:
        """Return Town daily weather data."""
        weather: dict[str, Any] = {}

        forecast = self.get_current_forecast()
        if forecast is not None:
            weather[AOD_CONDITION] = forecast.get_condition()
            weather[AOD_PRECIPITATION_PROBABILITY] = forecast.get_precipitation_prob()
            weather[AOD_UV_INDEX] = forecast.get_uv_index()
            weather[AOD_WIND_DIRECTION] = forecast.get_wind_direction()
            weather[AOD_WIND_SPEED] = forecast.get_wind_speed()

        return weather


class HourlyForecast:
    """AEMET OpenData Town Hourly Forecast."""

    _datetime: datetime
    forecast: list[HourlyForecastValue]
    zoneinfo: ZoneInfo

    def __init__(self, data: dict[str, Any], zoneinfo: ZoneInfo) -> None:
        """Init AEMET OpenData Town Hourly Forecast."""

        self._datetime = parse_api_timestamp(data[AEMET_ATTR_ELABORATED])
        self.forecast: list[HourlyForecastValue] = []
        self.zoneinfo = zoneinfo

        cur_dt = get_current_datetime(zoneinfo)
        cur_day = cur_dt.date()
        cur_hour = cur_dt.hour

        for day_data in data[AEMET_ATTR_FORECAST][AEMET_ATTR_DAY]:
            day = parse_api_timestamp(day_data[AEMET_ATTR_DATE], zoneinfo)
            day_date = day.date()
            if cur_day <= day_date:
                if cur_day == day_date:
                    start_hour = cur_hour
                else:
                    start_hour = 0

                for hour in range(start_hour, 24):
                    try:
                        cur_forecast = HourlyForecastValue(day_data, day, hour)
                        self.forecast += [cur_forecast]
                    except ValueError as err:
                        _LOGGER.debug(err)

    def get_current_forecast(self) -> HourlyForecastValue | None:
        """Return Town current hourly forecast."""
        cur_dt = get_current_datetime(self.get_timezone())
        for forecast in self.forecast:
            forecast_dt = forecast.get_datetime()
            if cur_dt == forecast_dt:
                return forecast
        return None

    def get_timestamp(self) -> str:
        """Return Town hourly forecast timestamp."""
        return self._datetime.isoformat()

    def get_timestamp_local(self) -> str:
        """Return Town daily forecast timestamp."""
        return self._datetime.isoformat()

    def get_timestamp_utc(self) -> str:
        """Return Town daily forecast timestamp."""
        return self._datetime.astimezone(timezone.utc).isoformat()

    def get_timezone(self) -> ZoneInfo:
        """Return Town hourly forecast timezone."""
        return self.zoneinfo

    def data(self) -> dict[str, Any]:
        """Return Town hourly forecast data."""
        data: dict[str, Any] = {
            AOD_FORECAST: [],
            AOD_TIMESTAMP_LOCAL: self.get_timestamp_local(),
            AOD_TIMESTAMP_UTC: self.get_timestamp_utc(),
            AOD_TIMEZONE: self.get_timezone(),
        }

        cur_dt = get_current_datetime(self.get_timezone())
        for forecast in self.forecast:
            forecast_dt = forecast.get_datetime()
            if cur_dt <= forecast_dt:
                data[AOD_FORECAST] += [forecast.data()]

        cur_forecast = self.get_current_forecast()
        if cur_forecast is not None:
            data[AOD_FORECAST_CURRENT] = cur_forecast.data()

        return data

    def weather(self) -> dict[str, Any]:
        """Return Town hourly weather data."""
        weather: dict[str, Any] = {}

        forecast = self.get_current_forecast()
        if forecast is not None:
            weather[AOD_FEEL_TEMP] = forecast.get_feel_temp()
            weather[AOD_CONDITION] = forecast.get_condition()
            weather[AOD_HUMIDITY] = forecast.get_humidity()
            weather[AOD_PRECIPITATION] = forecast.get_precipitation()
            weather[AOD_PRECIPITATION_PROBABILITY] = (
                forecast.get_precipitation_probability()
            )
            weather[AOD_TEMP] = forecast.get_temp()
            weather[AOD_RAIN] = forecast.get_rain()
            weather[AOD_RAIN_PROBABILITY] = forecast.get_rain_probability()
            weather[AOD_SNOW] = forecast.get_snow()
            weather[AOD_SNOW_PROBABILITY] = forecast.get_snow_probability()
            weather[AOD_STORM_PROBABILITY] = forecast.get_storm_probability()
            weather[AOD_WIND_DIRECTION] = forecast.get_wind_direction()
            weather[AOD_WIND_SPEED] = forecast.get_wind_speed()
            weather[AOD_WIND_SPEED_MAX] = forecast.get_wind_speed_max()

        return weather


class Town:
    """AEMET OpenData Town."""

    altitude: int
    coords: tuple[float, float]
    daily: DailyForecast | None
    distance: float
    id: str
    name: str
    residents: int
    zoneinfo: ZoneInfo

    def __init__(self, data: dict[str, Any]) -> None:
        """Init AEMET OpenData Town."""
        self.altitude = int(data[AEMET_ATTR_TOWN_ALTITUDE])
        self.coords = (
            float(data[AEMET_ATTR_TOWN_LATITUDE_DECIMAL]),
            float(data[AEMET_ATTR_TOWN_LONGITUDE_DECIMAL]),
        )
        self.daily: DailyForecast | None = None
        self.distance = float(data[ATTR_DISTANCE])
        self.hourly: HourlyForecast | None = None
        self.id = str(data[AEMET_ATTR_ID])
        self.name = str(data[AEMET_ATTR_NAME])
        self.residents = int(data[AEMET_ATTR_TOWN_RESIDENTS])
        self.zoneinfo = timezone_from_coords(self.coords)

    def get_altitude(self) -> int:
        """Return Town altitude."""
        return self.altitude

    def get_coords(self) -> tuple[float, float]:
        """Return Town coordinates."""
        return self.coords

    def get_distance(self) -> float:
        """Return Town distance from selected coordinates."""
        return round(self.distance, 3)

    def get_id(self) -> str:
        """Return Town ID."""
        return self.id

    def get_residents(self) -> int:
        """Return Town residents."""
        return self.residents

    def get_name(self) -> str:
        """Return Town name."""
        return self.name

    def get_timezone(self) -> ZoneInfo:
        """Return Town zoneinfo."""
        return self.zoneinfo

    def update_daily(self, forecast: dict[str, Any]) -> None:
        """Update Town daily forecast."""
        self.daily = DailyForecast(forecast[ATTR_DATA][0], self.get_timezone())

    def update_hourly(self, forecast: dict[str, Any]) -> None:
        """Update Town hourly forecast."""
        self.hourly = HourlyForecast(forecast[ATTR_DATA][0], self.get_timezone())

    def data(self) -> dict[str, Any]:
        """Return Town data."""
        data: dict[str, Any] = {
            AOD_ALTITUDE: self.get_altitude(),
            AOD_COORDS: self.get_coords(),
            AOD_DISTANCE: self.get_distance(),
            AOD_ID: self.get_id(),
            AOD_NAME: self.get_name(),
            AOD_RESIDENTS: self.get_residents(),
            AOD_TIMEZONE: self.get_timezone(),
        }

        if self.daily is not None:
            data[AOD_FORECAST_DAILY] = self.daily.data()

        if self.hourly is not None:
            data[AOD_FORECAST_HOURLY] = self.hourly.data()

        return data

    def weather_daily(self) -> dict[str, Any]:
        """Return Town daily weather data."""
        if self.daily is not None:
            return self.daily.weather()
        return {}

    def weather_hourly(self) -> dict[str, Any]:
        """Return Town hourly weather data."""
        if self.hourly is not None:
            return self.hourly.weather()
        return {}
