"""AEMET OpenData Helpers."""

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .const import (
    AEMET_ATTR_PERIOD,
    AEMET_ATTR_VALUE,
    API_ID_PFX,
    API_PERIOD_24H,
    API_PERIOD_FULL_DAY,
    API_PERIOD_SPLIT,
)

TZ_UTC = ZoneInfo("UTC")


def dict_nested_value(data: dict[str, Any] | None, keys: list[str] | None) -> Any:
    """Get value from dict with nested keys."""
    if keys is None or len(keys) == 0:
        return None
    for key in keys or {}:
        if data is not None:
            data = data.get(key)
    return data


def get_current_datetime(tz: ZoneInfo = TZ_UTC) -> datetime:
    """Return current datetime in UTC."""
    return datetime.now(tz=tz).replace(minute=0, second=0, microsecond=0)


def get_forecast_day_value(
    values: dict[str, Any] | list[Any], key: str = AEMET_ATTR_VALUE
) -> Any:
    """Get day value from forecast."""
    if isinstance(values, list):
        if len(values) > 1:
            for value in values:
                if key not in value:
                    continue
                if value[AEMET_ATTR_PERIOD] == API_PERIOD_FULL_DAY:
                    return value[key]
        else:
            if key in values[0]:
                return values[0][key]
    if isinstance(values, dict):
        if key in values:
            return values[key]
    return None


def get_forecast_hour_value(values: Any, hour: int, key: str = AEMET_ATTR_VALUE) -> Any:
    """Get hour value from forecast."""
    for value in values:
        if key not in value:
            continue
        if int(value[AEMET_ATTR_PERIOD]) == hour:
            return None if not value[key] else value[key]
    return None


def get_forecast_interval_value(
    values: Any, hour: int, key: str = AEMET_ATTR_VALUE
) -> Any:
    """Get hour value from forecast interval."""
    for value in values:
        if key not in value:
            continue
        period_start = int(value[AEMET_ATTR_PERIOD][0:API_PERIOD_SPLIT])
        period_end = int(
            value[AEMET_ATTR_PERIOD][API_PERIOD_SPLIT : API_PERIOD_SPLIT * 2]
        )
        if period_end < period_start:
            period_end = period_end + API_PERIOD_24H
            if hour == 0:
                hour = hour + API_PERIOD_24H
        if period_start <= hour < period_end:
            return None if not value[key] else value[key]
    return None


def split_coordinate(coordinate: str) -> str:
    """Split climatological values station coordinate."""
    coord_deg = coordinate[0:2]
    coord_min = coordinate[2:4]
    coord_sec = coordinate[4:6]
    coord_dir = coordinate[6:7]
    return f"{coord_deg} {coord_min}m {coord_sec}s {coord_dir}"


def parse_api_timestamp(timestamp: str, tz: ZoneInfo = TZ_UTC) -> datetime:
    """Parse AEMET OpenData timestamp into datetime."""
    return datetime.fromisoformat(timestamp).replace(tzinfo=tz)


def parse_station_coordinates(latitude: str, longitude: str) -> str:
    """Parse climatological values station coordinates."""
    return f"{split_coordinate(latitude)} {split_coordinate(longitude)}"


def parse_town_code(town_id: str) -> str:
    """Parse town code from ID if needed."""
    if isinstance(town_id, str) and town_id.startswith(API_ID_PFX):
        return town_id[len(API_ID_PFX) :]
    return town_id


def timezone_from_coords(coords: tuple[float, float]) -> ZoneInfo:
    """Convert coordinates to timezone."""
    if coords[0] < 32 and coords[1] < -11.5:
        return ZoneInfo("Atlantic/Canary")
    return ZoneInfo("Europe/Madrid")
