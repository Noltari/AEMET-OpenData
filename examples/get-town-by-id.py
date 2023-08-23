"""Get AEMET OpenData town data by ID example."""
import asyncio
import json
import timeit

import _secrets
import aiohttp

from aemet_opendata.exceptions import AuthError
from aemet_opendata.interface import AEMET


async def main():
    """AEMET OpenData client example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        client = AEMET(aiohttp_session, _secrets.AEMET_OPTIONS)

        try:
            get_town_start = timeit.default_timer()
            town = await client.get_town(town="id28065")
            get_town_end = timeit.default_timer()
            print(json.dumps(town, indent=4, sort_keys=True))
            print(f"Get Town time: {get_town_end - get_town_start}")
        except AuthError:
            print("API authentication error.")


if __name__ == "__main__":
    asyncio.run(main())
