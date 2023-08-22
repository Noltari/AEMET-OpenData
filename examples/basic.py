"""Basic AEMET OpenData client example."""
import asyncio
import json
import timeit

import _secrets
import aiohttp

from aemet_opendata.exceptions import (
    AuthError,
    StationNotFound,
    TooManyRequests,
    TownNotFound,
)
from aemet_opendata.interface import AEMET


async def main():
    """AEMET OpenData client example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        client = AEMET(aiohttp_session, _secrets.AEMET_OPTIONS)

        try:
            select_start = timeit.default_timer()
            coords_data = await client.select_coordinates(40.3049863, -3.7550013)
            select_end = timeit.default_timer()
            print(json.dumps(coords_data, indent=4, sort_keys=True))
            print(f"Select time: {select_end - select_start}")
            print("***")

            update_start = timeit.default_timer()
            await client.update()
            update_end = timeit.default_timer()
            print(json.dumps(client.data(), indent=4, sort_keys=True))
            print(f"Update time: {update_end - update_start}")
        except AuthError:
            print("API authentication error.")
        except StationNotFound:
            print("Station not found.")
        except TooManyRequests:
            print("Too many requests.")
        except TownNotFound:
            print("Town not found.")


if __name__ == "__main__":
    asyncio.run(main())
