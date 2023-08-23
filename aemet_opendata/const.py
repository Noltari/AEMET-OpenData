"""AEMET OpenData Constants."""

from typing import Final

AEMET_ATTR_DATA: Final[str] = "datos"
AEMET_ATTR_DATE: Final[str] = "fecha"
AEMET_ATTR_DAY: Final[str] = "dia"
AEMET_ATTR_DIRECTION: Final[str] = "direccion"
AEMET_ATTR_ELABORATED: Final[str] = "elaborado"
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
AEMET_ATTR_STATION_TEMPERATURE_RELATIVE: Final[str] = "tpr"
AEMET_ATTR_STATION_WIND: Final[str] = "rviento"
AEMET_ATTR_STORM_PROBABILITY: Final[str] = "probTormenta"
AEMET_ATTR_SUN_RISE: Final[str] = "orto"
AEMET_ATTR_SUN_SET: Final[str] = "ocaso"
AEMET_ATTR_TEMPERATURE: Final[str] = "temperatura"
AEMET_ATTR_TEMPERATURE_FEELING: Final[str] = "sensTermica"
AEMET_ATTR_TOWN_LATITUDE: Final[str] = "latitud"
AEMET_ATTR_TOWN_LATITUDE_DECIMAL: Final[str] = "latitud_dec"
AEMET_ATTR_TOWN_LONGITUDE: Final[str] = "longitud"
AEMET_ATTR_TOWN_LONGITUDE_DECIMAL: Final[str] = "longitud_dec"
AEMET_ATTR_VALUE: Final[str] = "value"
AEMET_ATTR_WEATHER_STATION_LATITUDE: Final[str] = "latitud"
AEMET_ATTR_WEATHER_STATION_LONGITUDE: Final[str] = "longitud"
AEMET_ATTR_WIND: Final[str] = "viento"
AEMET_ATTR_WIND_GUST: Final[str] = "vientoAndRachaMax"

API_ID_PFX: Final[str] = "id"
API_MIN_STATION_DISTANCE_KM: Final[int] = 40
API_MIN_TOWN_DISTANCE_KM: Final[int] = 40
API_PERIOD_24H: Final[int] = 24
API_PERIOD_FULL_DAY: Final[str] = "00-24"
API_PERIOD_SPLIT: Final[int] = 2
API_TIMEOUT: Final[int] = 15
API_URL: Final[str] = "https://opendata.aemet.es/opendata/api"

ATTR_DATA: Final[str] = "data"
ATTR_RESPONSE: Final[str] = "response"

RAW_FORECAST_DAILY: Final[str] = "forecast-daily"
RAW_FORECAST_HOURLY: Final[str] = "forecast-hourly"
RAW_STATIONS: Final[str] = "stations"
RAW_TOWNS: Final[str] = "towns"
