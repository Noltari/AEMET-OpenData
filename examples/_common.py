"""AEMET OpenData Examples."""

import json
from typing import Any


def json_dumps(data: Any) -> str:
    """Dump data using json.dumps()."""
    return json.dumps(data, indent=4, sort_keys=True, default=str)
