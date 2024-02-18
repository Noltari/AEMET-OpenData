"""Basic AEMET OpenData client example."""

import asyncio
import timeit

from _common import json_dumps
from _secrets import AEMET_COORDS, AEMET_OPTIONS
import aiohttp

from aemet_opendata.exceptions import ApiError, AuthError, TooManyRequests, TownNotFound
from aemet_opendata.interface import AEMET


async def main():
    """AEMET OpenData client example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        client = AEMET(aiohttp_session, AEMET_OPTIONS)

        try:
            select_start = timeit.default_timer()
            await client.select_coordinates(AEMET_COORDS[0], AEMET_COORDS[1])
            select_end = timeit.default_timer()
            print(json_dumps(client.data()))
            print(f"Select time: {select_end - select_start}")
            print("***")

            update_start = timeit.default_timer()
            await client.update()
            update_end = timeit.default_timer()
            print(json_dumps(client.data()))
            print(f"Update time: {update_end - update_start}")
        except ApiError:
            print("API data error")
        except AuthError:
            print("API authentication error.")
        except TooManyRequests:
            print("Too many requests.")
        except TownNotFound:
            print("Town not found.")


if __name__ == "__main__":
    asyncio.run(main())
