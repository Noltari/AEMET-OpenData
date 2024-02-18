"""Get AEMET OpenData town data by coords example."""

import asyncio
import timeit

from _common import json_dumps
from _secrets import AEMET_COORDS, AEMET_OPTIONS
import aiohttp

from aemet_opendata.exceptions import AuthError
from aemet_opendata.interface import AEMET


async def main():
    """AEMET OpenData client example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        client = AEMET(aiohttp_session, AEMET_OPTIONS)

        client.distance_high_precision(True)

        try:
            get_town_start = timeit.default_timer()
            town = await client.get_town_by_coordinates(
                AEMET_COORDS[0], AEMET_COORDS[1]
            )
            get_town_end = timeit.default_timer()
            print(json_dumps(town))
            print(f"Get Town time: {get_town_end - get_town_start}")
        except AuthError:
            print("API authentication error.")


if __name__ == "__main__":
    asyncio.run(main())
