# -*- coding: utf-8 -*-
"""AEMET OpenData Helpers"""

from .const import API_ID_PFX


def parse_town_code(town_id):
    """Parses town code from ID if needed"""
    if isinstance(town_id, str) and town_id.startswith(API_ID_PFX):
        return town_id[len(API_ID_PFX) :]
    return town_id
