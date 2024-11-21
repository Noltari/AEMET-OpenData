"""AEMET OpenData Secrets."""

from aemet_opendata.interface import ConnectionOptions

AEMET_COORDS = (40.3049863, -3.7550013)
AEMET_DATA_DIR = "api-data"
AEMET_OPTIONS = ConnectionOptions(
    api_key="MY_API_KEY",
    station_data=True,
)
AEMET_TOWN = "id28065"
