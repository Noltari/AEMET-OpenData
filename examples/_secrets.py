"""AEMET OpenData Secrets."""

from aemet_opendata.interface import ConnectionOptions, UpdateFeature

AEMET_COORDS = (40.3049863, -3.7550013)
AEMET_DATA_DIR = "api-data"
AEMET_OPTIONS = ConnectionOptions(
    api_key="MY_API_KEY",
    update_features=UpdateFeature.STATION | UpdateFeature.RADAR,
)
AEMET_TOWN = "id28065"
