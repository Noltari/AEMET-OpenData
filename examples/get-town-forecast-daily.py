"""Get AEMET OpenData town daily forecast example."""

import asyncio
import timeit

from _common import json_dumps
from _secrets import AEMET_DATA_DIR, AEMET_OPTIONS, AEMET_TOWN
import aiohttp

from aemet_opendata.exceptions import AuthError
from aemet_opendata.interface import AEMET


async def main():
    """AEMET OpenData client example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        client = AEMET(aiohttp_session, AEMET_OPTIONS)

        client.set_api_data_dir(AEMET_DATA_DIR)

        try:
            get_forecast_start = timeit.default_timer()
            forecast = await client.get_specific_forecast_town_daily(AEMET_TOWN)
            get_forecast_end = timeit.default_timer()
            print(json_dumps(forecast))
            print(f"Get forecast time: {get_forecast_end - get_forecast_start}")
        except AuthError:
            print("API authentication error.")


if __name__ == "__main__":
    asyncio.run(main())
