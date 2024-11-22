"""AEMET OpenData Radar."""

from datetime import datetime
from typing import Any

from .const import (
    AOD_DATETIME,
    AOD_ID,
    AOD_IMG_BYTES,
    AOD_IMG_TYPE,
    ATTR_BYTES,
    ATTR_DATA,
    ATTR_TIMESTAMP,
    ATTR_TYPE,
)


class Radar:
    """AEMET OpenData Radar."""

    _datetime: datetime | None
    id: str
    img_bytes: bytes | None
    img_type: str | None

    def __init__(self, radar_id: str, radar_data: dict[str, Any]) -> None:
        """Init AEMET OpenData Radar."""

        self._datetime = None
        self.id = radar_id
        self.img_bytes = None
        self.img_type = None

        self.update(radar_data)

    def get_datetime(self) -> datetime | None:
        """Return Station datetime of data."""
        return self._datetime

    def get_id(self) -> str:
        """Return Radar ID."""
        return self.id

    def get_image_bytes(self) -> bytes | None:
        """Return Radar image bytes."""
        return self.img_bytes

    def get_image_type(self) -> str | None:
        """Return Radar image type."""
        return self.img_type

    def update(self, radar: dict[str, Any]) -> None:
        """Update Radar data from samples."""
        radar_data = radar.get(ATTR_DATA)
        if radar_data is None:
            return

        radar_timestamp = radar.get(ATTR_TIMESTAMP)
        if radar_timestamp is None:
            return

        self._datetime = datetime.fromisoformat(radar_timestamp)
        self.img_bytes = radar_data.get(ATTR_BYTES)
        self.img_type = radar_data.get(ATTR_TYPE)

    def data(self) -> dict[str, Any]:
        """Return Radar data."""
        data: dict[str, Any] = {
            AOD_ID: self.get_id(),
        }

        _datetime = self.get_datetime()
        if _datetime is not None:
            data[AOD_DATETIME] = _datetime

        img_bytes = self.get_image_bytes()
        if img_bytes is not None:
            data[AOD_IMG_BYTES] = img_bytes

        img_type = self.get_image_type()
        if img_type is not None:
            data[AOD_IMG_TYPE] = img_type

        return data
