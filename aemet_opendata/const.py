"""AEMET OpenData Constants."""

from datetime import timedelta
from typing import Final

AEMET_ATTR_DATA: Final[str] = "datos"
AEMET_ATTR_DATE: Final[str] = "fecha"
AEMET_ATTR_DAY: Final[str] = "dia"
AEMET_ATTR_DIRECTION: Final[str] = "direccion"
AEMET_ATTR_ELABORATED: Final[str] = "elaborado"
AEMET_ATTR_FEEL_TEMPERATURE: Final[str] = "sensTermica"
AEMET_ATTR_FORECAST: Final[str] = "prediccion"
AEMET_ATTR_GUST: Final[str] = "rachaMax"
AEMET_ATTR_HUMIDITY: Final[str] = "humedadRelativa"
AEMET_ATTR_ID: Final[str] = "id"
AEMET_ATTR_IDEMA: Final[str] = "idema"
AEMET_ATTR_MAX: Final[str] = "maxima"
AEMET_ATTR_MIN: Final[str] = "minima"
AEMET_ATTR_NAME: Final[str] = "nombre"
AEMET_ATTR_PERIOD: Final[str] = "periodo"
AEMET_ATTR_PRECIPITATION: Final[str] = "precipitacion"
AEMET_ATTR_PRECIPITATION_PROBABILITY: Final[str] = "probPrecipitacion"
AEMET_ATTR_SKY_STATE: Final[str] = "estadoCielo"
AEMET_ATTR_SNOW: Final[str] = "nieve"
AEMET_ATTR_SNOW_PROBABILITY: Final[str] = "probNieve"
AEMET_ATTR_SPEED: Final[str] = "velocidad"
AEMET_ATTR_STATION_ALTITUDE: Final[str] = "alt"
AEMET_ATTR_STATION_DATE: Final[str] = "fint"
AEMET_ATTR_STATION_DEWPOINT: Final[str] = "tpr"
AEMET_ATTR_STATION_HUMIDITY: Final[str] = "hr"
AEMET_ATTR_STATION_LATITUDE: Final[str] = "lat"
AEMET_ATTR_STATION_LOCATION: Final[str] = "ubi"
AEMET_ATTR_STATION_LONGITUDE: Final[str] = "lon"
AEMET_ATTR_STATION_PRECIPITATION: Final[str] = "prec"
AEMET_ATTR_STATION_PRESSURE: Final[str] = "pres"
AEMET_ATTR_STATION_PRESSURE_SEA: Final[str] = "pres_nmar"
AEMET_ATTR_STATION_TEMPERATURE: Final[str] = "ta"
AEMET_ATTR_STATION_TEMPERATURE_MAX: Final[str] = "tamax"
AEMET_ATTR_STATION_TEMPERATURE_MIN: Final[str] = "tamin"
AEMET_ATTR_STATION_WIND_DIRECTION: Final[str] = "dv"
AEMET_ATTR_STATION_WIND_SPEED: Final[str] = "vv"
AEMET_ATTR_STATION_WIND_SPEED_MAX: Final[str] = "vmax"
AEMET_ATTR_STATE: Final[str] = "estado"
AEMET_ATTR_STORM_PROBABILITY: Final[str] = "probTormenta"
AEMET_ATTR_SUN_RISE: Final[str] = "orto"
AEMET_ATTR_SUN_SET: Final[str] = "ocaso"
AEMET_ATTR_TEMPERATURE: Final[str] = "temperatura"
AEMET_ATTR_TOWN_ALTITUDE: Final[str] = "altitud"
AEMET_ATTR_TOWN_RESIDENTS: Final[str] = "num_hab"
AEMET_ATTR_TOWN_LATITUDE: Final[str] = "latitud"
AEMET_ATTR_TOWN_LATITUDE_DECIMAL: Final[str] = "latitud_dec"
AEMET_ATTR_TOWN_LONGITUDE: Final[str] = "longitud"
AEMET_ATTR_TOWN_LONGITUDE_DECIMAL: Final[str] = "longitud_dec"
AEMET_ATTR_UV_MAX: Final[str] = "uvMax"
AEMET_ATTR_VALUE: Final[str] = "value"
AEMET_ATTR_WEATHER_STATION_LATITUDE: Final[str] = "latitud"
AEMET_ATTR_WEATHER_STATION_LONGITUDE: Final[str] = "longitud"
AEMET_ATTR_WIND: Final[str] = "viento"
AEMET_ATTR_WIND_GUST: Final[str] = "vientoAndRachaMax"

AOD_ALTITUDE: Final[str] = "altitude"
AOD_COND_CLEAR_NIGHT: Final[str] = "clear-night"
AOD_COND_CLOUDY: Final[str] = "cloudy"
AOD_COND_FOG: Final[str] = "fog"
AOD_COND_LIGHTNING: Final[str] = "lightning"
AOD_COND_LIGHTNING_RAINY: Final[str] = "lightning-rainy"
AOD_COND_PARTLY_CLODUY: Final[str] = "partly-cloudy"
AOD_COND_POURING: Final[str] = "pouring"
AOD_COND_RAINY: Final[str] = "rainy"
AOD_COND_SNOWY: Final[str] = "snowy"
AOD_COND_SUNNY: Final[str] = "sunny"
AOD_CONDITION: Final[str] = "condition"
AOD_COORDS: Final[str] = "coordinates"
AOD_DATETIME: Final[str] = "datetime"
AOD_DEW_POINT: Final[str] = "dew-point"
AOD_DISTANCE: Final[str] = "distance"
AOD_FEEL_TEMP: Final[str] = "feel-temperature"
AOD_FEEL_TEMP_MAX: Final[str] = "feel-temperature-max"
AOD_FEEL_TEMP_MIN: Final[str] = "feel-temperature-min"
AOD_FORECAST: Final[str] = "forecast"
AOD_FORECAST_CURRENT: Final[str] = "forecast-current"
AOD_FORECAST_DAILY: Final[str] = "forecast-daily"
AOD_FORECAST_HOURLY: Final[str] = "forecast-hourly"
AOD_HUMIDITY: Final[str] = "humidity"
AOD_HUMIDITY_MAX: Final[str] = "humidity-max"
AOD_HUMIDITY_MIN: Final[str] = "humidity-min"
AOD_ID: Final[str] = "id"
AOD_IMG_BYTES: Final[str] = "image-bytes"
AOD_IMG_TYPE: Final[str] = "image-type"
AOD_NAME: Final[str] = "name"
AOD_OUTDATED: Final[str] = "outdated"
AOD_RADAR: Final[str] = "radar"
AOD_RAIN: Final[str] = "rain"
AOD_RAIN_PROBABILITY: Final[str] = "rain-probability"
AOD_PRECIPITATION: Final[str] = "precipitation"
AOD_PRECIPITATION_PROBABILITY: Final[str] = "precipitation-probability"
AOD_PRESSURE: Final[str] = "pressure"
AOD_RESIDENTS: Final[str] = "residents"
AOD_SNOW: Final[str] = "snow"
AOD_SNOW_PROBABILITY: Final[str] = "snow-probability"
AOD_STATION: Final[str] = "station"
AOD_STORM_PROBABILITY: Final[str] = "storm-probability"
AOD_SUNRISE: Final[str] = "sunrise"
AOD_SUNSET: Final[str] = "sunset"
AOD_TEMP: Final[str] = "temperature"
AOD_TEMP_FEELING: Final[str] = "temperature-feeling"
AOD_TEMP_MAX: Final[str] = "temperature-max"
AOD_TEMP_MIN: Final[str] = "temperature-min"
AOD_TIMESTAMP_LOCAL: Final[str] = "timestamp-local"
AOD_TIMESTAMP_UTC: Final[str] = "timestamp-utc"
AOD_TIMEZONE: Final[str] = "timezone"
AOD_TOWN: Final[str] = "town"
AOD_UV_INDEX: Final[str] = "uv-index"
AOD_WEATHER: Final[str] = "weather"
AOD_WIND_DIRECTION: Final[str] = "wind-direction"
AOD_WIND_SPEED: Final[str] = "wind-speed"
AOD_WIND_SPEED_MAX: Final[str] = "wind-speed-max"

API_CALL_FILE_EXTENSION: Final[str] = ".json"
API_CALL_DATA_TIMEOUT_DEF: Final[timedelta] = timedelta(hours=1)
API_HDR_REQ_COUNT: Final[str] = "Remaining-request-count"
API_ID_PFX: Final[str] = "id"
API_MIN_STATION_DISTANCE_KM: Final[int] = 40
API_MIN_TOWN_DISTANCE_KM: Final[int] = 40
API_PERIOD_24H: Final[int] = 24
API_PERIOD_FULL_DAY: Final[str] = "00-24"
API_PERIOD_HALF_1_DAY: Final[str] = "00-12"
API_PERIOD_HALF_2_DAY: Final[str] = "12-24"
API_PERIOD_QUARTER_1_DAY: Final[str] = "00-06"
API_PERIOD_QUARTER_2_DAY: Final[str] = "06-12"
API_PERIOD_QUARTER_3_DAY: Final[str] = "12-18"
API_PERIOD_QUARTER_4_DAY: Final[str] = "18-24"
API_PERIOD_SPLIT: Final[int] = 2
API_URL: Final[str] = "https://opendata.aemet.es/opendata/api"

ATTR_BYTES: Final[str] = "bytes"
ATTR_DATA: Final[str] = "data"
ATTR_DISTANCE: Final[str] = "distance"
ATTR_RESPONSE: Final[str] = "response"
ATTR_TIMESTAMP: Final[str] = "timestamp"
ATTR_TYPE: Final[str] = "type"

CONTENT_TYPE_IMG: Final[str] = "image/"

HTTP_CALL_TIMEOUT: Final[int] = 15
HTTP_MAX_REQUESTS: Final[int] = 3

RAW_FORECAST_DAILY: Final[str] = "forecast-daily"
RAW_FORECAST_HOURLY: Final[str] = "forecast-hourly"
RAW_REQ_COUNT: Final[str] = "requests-counter"
RAW_STATIONS: Final[str] = "stations"
RAW_TOWNS: Final[str] = "towns"

STATION_MAX_DELTA: Final[timedelta] = timedelta(hours=2)
