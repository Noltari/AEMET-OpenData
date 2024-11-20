"""Get AEMET OpenData weather radar map."""

import asyncio
import timeit

from _secrets import AEMET_OPTIONS
import aiohttp

from aemet_opendata.const import ATTR_BYTES, ATTR_DATA, ATTR_TYPE
from aemet_opendata.exceptions import AuthError
from aemet_opendata.helpers import parse_data_type_ext
from aemet_opendata.interface import AEMET


async def main():
    """AEMET OpenData client example."""

    async with aiohttp.ClientSession() as aiohttp_session:
        client = AEMET(aiohttp_session, AEMET_OPTIONS)

        try:
            api_start = timeit.default_timer()
            national_radar = await client.get_radar_map()
            api_end = timeit.default_timer()
            print(f"Get National Radar time: {api_end - api_start}")

            national_radar_data = national_radar.get(ATTR_DATA, {})
            file_ext = parse_data_type_ext(national_radar_data.get(ATTR_TYPE))

            with open(f"national-radar.{file_ext}", "wb") as national_radar_file:
                national_radar_file.write(national_radar_data.get(ATTR_BYTES))
                national_radar_file.close()
        except AuthError:
            print("API authentication error.")


if __name__ == "__main__":
    asyncio.run(main())
