"""AEMET OpenData Helpers."""

import base64
from datetime import datetime
import json
import re
from typing import Any
import unicodedata
from zoneinfo import ZoneInfo

from .const import API_ID_PFX, CONTENT_TYPE_IMG

TZ_UTC = ZoneInfo("UTC")


class BytesEncoder(json.JSONEncoder):
    """JSON Bytes Encoder class."""

    def default(self, o: Any) -> Any:
        """JSON default encoder function."""
        if isinstance(o, bytes):
            return base64.b64encode(o).decode("utf-8")
        return super().default(o)


def dict_nested_value(data: dict[str, Any] | None, keys: list[str] | None) -> Any:
    """Get value from dict with nested keys."""
    if keys is None or len(keys) == 0:
        return None
    for key in keys or {}:
        if data is not None:
            data = data.get(key)
    return data


def get_current_datetime(tz: ZoneInfo = TZ_UTC, replace: bool = True) -> datetime:
    """Return current datetime in UTC."""
    cur_dt = datetime.now(tz=tz)
    if replace:
        cur_dt = cur_dt.replace(minute=0, second=0, microsecond=0)
    return cur_dt


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


def parse_data_type_ext(data_type: str) -> str:
    """Parse AEMET OpenData data type file extension."""
    if data_type.startswith(CONTENT_TYPE_IMG):
        return data_type.removeprefix(CONTENT_TYPE_IMG)
    return ""


def parse_station_coordinates(latitude: str, longitude: str) -> str:
    """Parse climatological values station coordinates."""
    return f"{split_coordinate(latitude)} {split_coordinate(longitude)}"


def parse_town_code(town_id: str) -> str:
    """Parse town code from ID if needed."""
    if isinstance(town_id, str) and town_id.startswith(API_ID_PFX):
        return town_id[len(API_ID_PFX) :]
    return town_id


def slugify(value: str, allow_unicode: bool = False) -> str:
    """Convert string to a valid file name."""
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s]", "-", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def timezone_from_coords(coords: tuple[float, float]) -> ZoneInfo:
    """Convert coordinates to timezone."""
    if coords[0] < 32 and coords[1] < -11.5:
        return ZoneInfo("Atlantic/Canary")
    return ZoneInfo("Europe/Madrid")
