# -*- coding: utf-8 -*-
"""AEMET OpenData Helpers"""

from .const import API_ID_PFX


def split_coordinate(coordinate):
    """Split climatological values station coordinate"""
    coord_deg = coordinate[0:2]
    coord_min = coordinate[2:4]
    coord_sec = coordinate[4:6]
    coord_dir = coordinate[6:7]
    return "%s %sm %ss %s" % (coord_deg, coord_min, coord_sec, coord_dir)


def parse_station_coordinates(latitude, longitude):
    """Parses climatological values station coordinates"""
    return "%s %s" % (split_coordinate(latitude), split_coordinate(longitude))


def parse_town_code(town_id):
    """Parses town code from ID if needed"""
    if isinstance(town_id, str) and town_id.startswith(API_ID_PFX):
        return town_id[len(API_ID_PFX) :]
    return town_id
