"""Get AEMET OpenData town daily forecast example."""
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
            get_forecast_start = timeit.default_timer()
            forecast = await client.get_specific_forecast_town_daily("id28065")
            get_forecast_end = timeit.default_timer()
            print(json.dumps(forecast, indent=4, sort_keys=True))
            print(f"Get forecast time: {get_forecast_end - get_forecast_start}")
        except AuthError:
            print("API authentication error.")


if __name__ == "__main__":
    asyncio.run(main())
