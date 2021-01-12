# -*- coding: utf-8 -*-
"""AEMET OpenData Helpers."""

from .const import (
    AEMET_ATTR_PERIOD,
    AEMET_ATTR_VALUE,
    API_ID_PFX,
    API_PERIOD_24H,
    API_PERIOD_FULL_DAY,
    API_PERIOD_SPLIT,
)


def get_forecast_day_value(values, key: str = AEMET_ATTR_VALUE):
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


def get_forecast_hour_value(values, hour: int, key: str = AEMET_ATTR_VALUE):
    """Get hour value from forecast."""
    for value in values:
        if key not in value:
            continue
        if int(value[AEMET_ATTR_PERIOD]) == hour:
            return None if not value[key] else value[key]
    return None


def get_forecast_interval_value(values, hour: int, key: str = AEMET_ATTR_VALUE):
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


def split_coordinate(coordinate):
    """Split climatological values station coordinate."""
    coord_deg = coordinate[0:2]
    coord_min = coordinate[2:4]
    coord_sec = coordinate[4:6]
    coord_dir = coordinate[6:7]
    return "%s %sm %ss %s" % (coord_deg, coord_min, coord_sec, coord_dir)


def parse_station_coordinates(latitude, longitude):
    """Parse climatological values station coordinates."""
    return "%s %s" % (split_coordinate(latitude), split_coordinate(longitude))


def parse_town_code(town_id):
    """Parse town code from ID if needed."""
    if isinstance(town_id, str) and town_id.startswith(API_ID_PFX):
        return town_id[len(API_ID_PFX) :]
    return town_id
