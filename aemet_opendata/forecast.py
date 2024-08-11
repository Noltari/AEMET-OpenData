"""AEMET OpenData Forecast."""

from datetime import datetime, timezone
from typing import Any, Final

from .const import (
    AEMET_ATTR_DIRECTION,
    AEMET_ATTR_FEEL_TEMPERATURE,
    AEMET_ATTR_HUMIDITY,
    AEMET_ATTR_MAX,
    AEMET_ATTR_MIN,
    AEMET_ATTR_PERIOD,
    AEMET_ATTR_PRECIPITATION,
    AEMET_ATTR_PRECIPITATION_PROBABILITY,
    AEMET_ATTR_SKY_STATE,
    AEMET_ATTR_SNOW,
    AEMET_ATTR_SNOW_PROBABILITY,
    AEMET_ATTR_SPEED,
    AEMET_ATTR_STORM_PROBABILITY,
    AEMET_ATTR_SUN_RISE,
    AEMET_ATTR_SUN_SET,
    AEMET_ATTR_TEMPERATURE,
    AEMET_ATTR_UV_MAX,
    AEMET_ATTR_VALUE,
    AEMET_ATTR_WIND,
    AEMET_ATTR_WIND_GUST,
    AOD_COND_CLEAR_NIGHT,
    AOD_COND_CLOUDY,
    AOD_COND_FOG,
    AOD_COND_LIGHTNING,
    AOD_COND_LIGHTNING_RAINY,
    AOD_COND_PARTLY_CLODUY,
    AOD_COND_POURING,
    AOD_COND_RAINY,
    AOD_COND_SNOWY,
    AOD_COND_SUNNY,
    AOD_CONDITION,
    AOD_FEEL_TEMP,
    AOD_FEEL_TEMP_MAX,
    AOD_FEEL_TEMP_MIN,
    AOD_HUMIDITY,
    AOD_HUMIDITY_MAX,
    AOD_HUMIDITY_MIN,
    AOD_PRECIPITATION,
    AOD_PRECIPITATION_PROBABILITY,
    AOD_RAIN,
    AOD_RAIN_PROBABILITY,
    AOD_SNOW,
    AOD_SNOW_PROBABILITY,
    AOD_STORM_PROBABILITY,
    AOD_SUNRISE,
    AOD_SUNSET,
    AOD_TEMP,
    AOD_TEMP_MAX,
    AOD_TEMP_MIN,
    AOD_TIMESTAMP_LOCAL,
    AOD_TIMESTAMP_UTC,
    AOD_UV_INDEX,
    AOD_WIND_DIRECTION,
    AOD_WIND_SPEED,
    AOD_WIND_SPEED_MAX,
    API_PERIOD_24H,
    API_PERIOD_FULL_DAY,
    API_PERIOD_HALF_2_DAY,
    API_PERIOD_QUARTER_4_DAY,
    API_PERIOD_SPLIT,
)

API_CONDITIONS_MAP: Final[dict[str, list[str]]] = {
    AOD_COND_CLEAR_NIGHT: [
        "11n",  # Despejado (de noche)
    ],
    AOD_COND_CLOUDY: [
        "14",  # Nuboso
        "14n",  # Nuboso (de noche)
        "15",  # Muy nuboso
        "15n",  # Muy nuboso (de noche)
        "16",  # Cubierto
        "16n",  # Cubierto (de noche)
        "17",  # Nubes altas
        "17n",  # Nubes altas (de noche)
    ],
    AOD_COND_FOG: [
        "81",  # Niebla
        "81n",  # Niebla (de noche)
        "82",  # Bruma - Neblina
        "82n",  # Bruma - Neblina (de noche)
    ],
    AOD_COND_LIGHTNING: [
        "51",  # Intervalos nubosos con tormenta
        "51n",  # Intervalos nubosos con tormenta (de noche)
        "52",  # Nuboso con tormenta
        "52n",  # Nuboso con tormenta (de noche)
        "53",  # Muy nuboso con tormenta
        "53n",  # Muy nuboso con tormenta (de noche)
        "54",  # Cubierto con tormenta
        "54n",  # Cubierto con tormenta (de noche)
    ],
    AOD_COND_LIGHTNING_RAINY: [
        "61",  # Intervalos nubosos con tormenta y lluvia escasa
        "61n",  # Intervalos nubosos con tormenta y lluvia escasa (de noche)
        "62",  # Nuboso con tormenta y lluvia escasa
        "62n",  # Nuboso con tormenta y lluvia escasa (de noche)
        "63",  # Muy nuboso con tormenta y lluvia escasa
        "63n",  # Muy nuboso con tormenta y lluvia escasa (de noche)
        "64",  # Cubierto con tormenta y lluvia escasa
        "64n",  # Cubierto con tormenta y lluvia escasa (de noche)
    ],
    AOD_COND_PARTLY_CLODUY: [
        "12",  # Poco nuboso
        "12n",  # Poco nuboso (de noche)
        "13",  # Intervalos nubosos
        "13n",  # Intervalos nubosos (de noche)
    ],
    AOD_COND_POURING: [
        "27",  # Chubascos
        "27n",  # Chubascos (de noche)
    ],
    AOD_COND_RAINY: [
        "23",  # Intervalos nubosos con lluvia
        "23n",  # Intervalos nubosos con lluvia (de noche)
        "24",  # Nuboso con lluvia
        "24n",  # Nuboso con lluvia (de noche)
        "25",  # Muy nuboso con lluvia
        "25n",  # Muy nuboso con lluvia (de noche)
        "26",  # Cubierto con lluvia
        "26n",  # Cubierto con lluvia (de noche)
        "43",  # Intervalos nubosos con lluvia escasa
        "43n",  # Intervalos nubosos con lluvia escasa (de noche)
        "44",  # Nuboso con lluvia escasa
        "44n",  # Nuboso con lluvia escasa (de noche)
        "45",  # Muy nuboso con lluvia escasa
        "45n",  # Muy nuboso con lluvia escasa (de noche)
        "46",  # Cubierto con lluvia escasa
        "46n",  # Cubierto con lluvia escasa (de noche)
    ],
    AOD_COND_SNOWY: [
        "33",  # Intervalos nubosos con nieve
        "33n",  # Intervalos nubosos con nieve (de noche)
        "34",  # Nuboso con nieve
        "34n",  # Nuboso con nieve (de noche)
        "35",  # Muy nuboso con nieve
        "35n",  # Muy nuboso con nieve (de noche)
        "36",  # Cubierto con nieve
        "36n",  # Cubierto con nieve (de noche)
        "71",  # Intervalos nubosos con nieve escasa
        "71n",  # Intervalos nubosos con nieve escasa (de noche)
        "72",  # Nuboso con nieve escasa
        "72n",  # Nuboso con nieve escasa (de noche)
        "73",  # Muy nuboso con nieve escasa
        "73n",  # Muy nuboso con nieve escasa (de noche)
        "74",  # Cubierto con nieve escasa
        "74n",  # Cubierto con nieve escasa (de noche)
    ],
    AOD_COND_SUNNY: [
        "11",  # Despejado
    ],
}


WIND_DIRECTION_MAP: Final[dict[str, float | None]] = {
    "C": None,
    "N": 0.0,
    "NE": 45.0,
    "E": 90.0,
    "SE": 135.0,
    "S": 180.0,
    "SO": 225.0,
    "O": 270.0,
    "NO": 315.0,
}


def hash_api_conditions(conditions_map: dict[str, list[str]]) -> dict[str, str]:
    """Hash API conditions for faster access."""
    res: dict[str, Any] = {}
    for k, v in conditions_map.items():
        for c in v:
            res[c] = k
    return res


CONDITIONS_DICT: Final[dict[str, str]] = hash_api_conditions(API_CONDITIONS_MAP)


class ForecastValue:
    """AEMET OpenData Town Forecast value."""

    @classmethod
    def parse_condition(cls, condition: str) -> str:
        """Parse forecast condition from API to human readable."""
        return CONDITIONS_DICT.get(condition, condition)

    @classmethod
    def parse_precipitation(cls, precipitation: str | None) -> float | None:
        """Parse forecast precipitation into a float."""
        if precipitation is None:
            return None
        if precipitation == "Ip":
            return 0.0
        return float(precipitation)

    @classmethod
    def parse_wind_direction(cls, wind_direction: str) -> float | None:
        """Parse forecast wind direction into a float."""
        return WIND_DIRECTION_MAP.get(wind_direction)


class DailyForecastValue(ForecastValue):
    """AEMET OpenData Town Daily Forecast value."""

    condition: str
    _datetime: datetime
    feel_temp_max: int
    feel_temp_min: int
    humidity_max: int
    humidity_min: int
    periods: list[str] = [
        API_PERIOD_FULL_DAY,
        API_PERIOD_HALF_2_DAY,
        API_PERIOD_QUARTER_4_DAY,
    ]
    precipitation_prob: int
    temp_max: int
    temp_min: int
    uv_index: int | None
    wind_direction: float | None
    wind_speed: float | None

    def __init__(self, data: dict[str, Any], dt: datetime) -> None:
        """Init AEMET OpenData Town Daily Forecast."""
        condition = self.parse_value(data[AEMET_ATTR_SKY_STATE])
        if condition is None or not condition:
            raise ValueError(f"DailyForecastValue {dt}")

        self.condition = self.parse_condition(condition)
        self._datetime = dt
        self.feel_temp_max = int(
            self.parse_value(data[AEMET_ATTR_FEEL_TEMPERATURE], key=AEMET_ATTR_MAX)
        )
        self.feel_temp_min = int(
            self.parse_value(data[AEMET_ATTR_FEEL_TEMPERATURE], key=AEMET_ATTR_MIN)
        )
        self.humidity_max = int(
            self.parse_value(data[AEMET_ATTR_HUMIDITY], key=AEMET_ATTR_MAX)
        )
        self.humidity_min = int(
            self.parse_value(data[AEMET_ATTR_HUMIDITY], key=AEMET_ATTR_MIN)
        )
        self.precipitation_prob = int(
            self.parse_value(data[AEMET_ATTR_PRECIPITATION_PROBABILITY])
        )
        self.temp_max = int(
            self.parse_value(data[AEMET_ATTR_TEMPERATURE], key=AEMET_ATTR_MAX)
        )
        self.temp_min = int(
            self.parse_value(data[AEMET_ATTR_TEMPERATURE], key=AEMET_ATTR_MIN)
        )
        self.wind_direction = self.parse_wind_direction(
            self.parse_value(data[AEMET_ATTR_WIND], key=AEMET_ATTR_DIRECTION),
        )

        if self.wind_direction is not None:
            self.wind_speed = int(
                self.parse_value(data[AEMET_ATTR_WIND], key=AEMET_ATTR_SPEED)
            )
        else:
            self.wind_speed = None

        if AEMET_ATTR_UV_MAX in data:
            self.uv_index = int(data[AEMET_ATTR_UV_MAX])
        else:
            self.uv_index = None

    def get_condition(self) -> str | None:
        """Return Town daily forecast condition."""
        return self.condition

    def get_datetime(self) -> datetime:
        """Return Town daily forecast datetime."""
        return self._datetime

    def get_feel_temp_max(self) -> int:
        """Return Town daily forecast maximum feel temperature."""
        return self.feel_temp_max

    def get_feel_temp_min(self) -> int:
        """Return Town daily forecast minimum feel temperature."""
        return self.feel_temp_min

    def get_humidity_max(self) -> int:
        """Return Town daily forecast maximum humidity."""
        return self.humidity_max

    def get_humidity_min(self) -> int:
        """Return Town daily forecast minimum humidity."""
        return self.humidity_min

    def get_precipitation_prob(self) -> int:
        """Return Town daily forecast precipitation probability."""
        return self.precipitation_prob

    def get_temp_max(self) -> int:
        """Return Town daily forecast maximum temperature."""
        return self.temp_max

    def get_temp_min(self) -> int:
        """Return Town daily forecast minimum temperature."""
        return self.temp_min

    def get_timestamp_local(self) -> str:
        """Return Town daily forecast local timestamp."""
        return self._datetime.isoformat()

    def get_timestamp_utc(self) -> str:
        """Return Town daily forecast UTC timestamp."""
        return self._datetime.astimezone(timezone.utc).isoformat()

    def get_uv_index(self) -> int | None:
        """Return Town daily forecast UV index."""
        return self.uv_index

    def get_wind_direction(self) -> float | None:
        """Return Town daily forecast wind direction."""
        return self.wind_direction

    def get_wind_speed(self) -> float | None:
        """Return Town daily forecast wind speed."""
        return self.wind_speed

    def data(self) -> dict[str, Any]:
        """Return Town daily forecast data."""
        data: dict[str, Any] = {
            AOD_CONDITION: self.get_condition(),
            AOD_FEEL_TEMP_MAX: self.get_feel_temp_max(),
            AOD_FEEL_TEMP_MIN: self.get_feel_temp_min(),
            AOD_HUMIDITY_MAX: self.get_humidity_max(),
            AOD_HUMIDITY_MIN: self.get_humidity_min(),
            AOD_PRECIPITATION_PROBABILITY: self.get_precipitation_prob(),
            AOD_TEMP_MAX: self.get_temp_max(),
            AOD_TEMP_MIN: self.get_temp_min(),
            AOD_TIMESTAMP_LOCAL: self.get_timestamp_local(),
            AOD_TIMESTAMP_UTC: self.get_timestamp_utc(),
            AOD_UV_INDEX: self.get_uv_index(),
            AOD_WIND_DIRECTION: self.get_wind_direction(),
            AOD_WIND_SPEED: self.get_wind_speed(),
        }

        return data

    def parse_value(
        self, values: dict[str, Any] | list[Any], key: str = AEMET_ATTR_VALUE
    ) -> Any:
        """Parse Town daily forecast value from data."""
        if isinstance(values, list):
            if len(values) > 1:
                for value in values:
                    if key not in value:
                        continue
                    if isinstance(value[key], str) and not value[key]:
                        continue
                    for period in self.periods:
                        if value[AEMET_ATTR_PERIOD] == period:
                            return value[key]
            else:
                if key in values[0]:
                    return values[0][key]
        if isinstance(values, dict):
            if key in values:
                return values[key]
        return None


class HourlyForecastValue(ForecastValue):
    """AEMET OpenData Town Hourly Forecast value."""

    condition: str
    _datetime: datetime
    feel_temp: int | None
    humidity: int | None
    rain: float | None
    rain_probability: int | None
    snow: float | None
    snow_probability: int | None
    storm_probability: int | None
    sunrise: str
    sunset: str
    temp: int | None
    wind_direction: float | None
    wind_speed: float | None
    wind_speed_max: float | None

    def __init__(self, data: dict[str, Any], dt: datetime, hour: int) -> None:
        """Init AEMET OpenData Town Hourly Forecast."""
        condition = self.parse_value(data[AEMET_ATTR_SKY_STATE], hour)
        if condition is None:
            raise ValueError(f"HourlyForecastValue {dt} {hour}:00")

        self.condition = self.parse_condition(condition)
        self._datetime = dt.replace(hour=hour)
        self.sunrise = str(data[AEMET_ATTR_SUN_RISE])
        self.sunset = str(data[AEMET_ATTR_SUN_SET])

        feel_temp = self.parse_value(data[AEMET_ATTR_FEEL_TEMPERATURE], hour)
        if feel_temp is not None:
            self.feel_temp = int(feel_temp)
        else:
            self.feel_temp = None

        humidity = self.parse_value(data[AEMET_ATTR_HUMIDITY], hour)
        if humidity is not None:
            self.humidity = int(humidity)
        else:
            self.humidity = None

        temp = self.parse_value(data[AEMET_ATTR_TEMPERATURE], hour)
        if temp is not None:
            self.temp = int(temp)
        else:
            self.temp = None

        rain_probability = self.parse_interval_value(
            data[AEMET_ATTR_PRECIPITATION_PROBABILITY], hour
        )
        if rain_probability is not None:
            self.rain_probability = int(rain_probability)

            rain = self.parse_value(data[AEMET_ATTR_PRECIPITATION], hour)
            if rain is not None:
                self.rain = self.parse_precipitation(rain)
            else:
                self.rain = None
        else:
            self.rain = None
            self.rain_probability = None

        snow_probability = self.parse_interval_value(
            data[AEMET_ATTR_SNOW_PROBABILITY], hour
        )
        if snow_probability is not None:
            self.snow_probability = int(snow_probability)

            snow = self.parse_value(data[AEMET_ATTR_SNOW], hour)
            if snow is not None:
                self.snow = self.parse_precipitation(snow)
            else:
                self.snow = None
        else:
            self.snow = None
            self.snow_probability = None

        storm_probability = self.parse_interval_value(
            data[AEMET_ATTR_STORM_PROBABILITY], hour
        )
        if storm_probability is not None:
            self.storm_probability = int(storm_probability)
        else:
            self.storm_probability = None

        wind_direction = self.parse_value(
            data[AEMET_ATTR_WIND_GUST],
            hour,
            key=AEMET_ATTR_DIRECTION,
        )
        if wind_direction is not None:
            self.wind_direction = self.parse_wind_direction(wind_direction[0])
        else:
            self.wind_direction = None

        if self.wind_direction is not None:
            self.wind_speed = float(
                self.parse_value(
                    data[AEMET_ATTR_WIND_GUST], hour, key=AEMET_ATTR_SPEED
                )[0]
            )
            self.wind_speed_max = float(
                self.parse_value(data[AEMET_ATTR_WIND_GUST], hour)
            )
        else:
            self.wind_speed = None
            self.wind_speed_max = None

    def get_condition(self) -> str:
        """Return Town hourly forecast condition."""
        return self.condition

    def get_datetime(self) -> datetime:
        """Return Town hourly forecast datetime."""
        return self._datetime

    def get_feel_temp(self) -> int | None:
        """Return Town hourly forecast feel temperature."""
        return self.feel_temp

    def get_humidity(self) -> int | None:
        """Return Town hourly forecast humidity."""
        return self.humidity

    def get_precipitation(self) -> float | None:
        """Return Town hourly forecast precipitation."""
        rain = self.get_rain()
        snow = self.get_snow()
        if rain is not None or snow is not None:
            rain = rain or 0.0
            snow = snow or 0.0
            return rain + snow
        return None

    def get_precipitation_probability(self) -> int | None:
        """Return Town hourly forecast precipitation probability."""
        rain_prob = self.get_rain_probability()
        snow_prob = self.get_snow_probability()
        if rain_prob is not None or snow_prob is not None:
            rain_prob = rain_prob or 0
            snow_prob = snow_prob or 0
            return max(rain_prob, snow_prob)
        return None

    def get_rain(self) -> float | None:
        """Return Town hourly forecast rain."""
        return self.rain

    def get_rain_probability(self) -> int | None:
        """Return Town hourly forecast rain probability."""
        return self.rain_probability

    def get_snow(self) -> float | None:
        """Return Town hourly forecast snow."""
        return self.snow

    def get_snow_probability(self) -> int | None:
        """Return Town hourly forecast snow probability."""
        return self.snow_probability

    def get_storm_probability(self) -> int | None:
        """Return Town hourly forecast storm probability."""
        return self.storm_probability

    def get_sunrise(self) -> str:
        """Return Town hourly forecast sunrise."""
        return self.sunrise

    def get_sunset(self) -> str:
        """Return Town hourly forecast sunset."""
        return self.sunset

    def get_temp(self) -> int | None:
        """Return Town hourly forecast temperature."""
        return self.temp

    def get_timestamp_local(self) -> str:
        """Return Town hourly forecast local timestamp."""
        return self._datetime.isoformat()

    def get_timestamp_utc(self) -> str:
        """Return Town hourly forecast UTC timestamp."""
        return self._datetime.astimezone(timezone.utc).isoformat()

    def get_wind_direction(self) -> float | None:
        """Return Town hourly forecast wind direction."""
        return self.wind_direction

    def get_wind_speed(self) -> float | None:
        """Return Town hourly forecast wind speed."""
        return self.wind_speed

    def get_wind_speed_max(self) -> float | None:
        """Return Town hourly forecast maximum wind speed."""
        return self.wind_speed_max

    def data(self) -> dict[str, Any]:
        """Return Town hourly forecast data."""
        data: dict[str, Any] = {
            AOD_CONDITION: self.get_condition(),
            AOD_FEEL_TEMP: self.get_feel_temp(),
            AOD_HUMIDITY: self.get_humidity(),
            AOD_PRECIPITATION: self.get_precipitation(),
            AOD_PRECIPITATION_PROBABILITY: self.get_precipitation_probability(),
            AOD_RAIN: self.get_rain(),
            AOD_RAIN_PROBABILITY: self.get_rain_probability(),
            AOD_SNOW: self.get_snow(),
            AOD_SNOW_PROBABILITY: self.get_snow_probability(),
            AOD_STORM_PROBABILITY: self.get_storm_probability(),
            AOD_SUNRISE: self.get_sunrise(),
            AOD_SUNSET: self.get_sunset(),
            AOD_TEMP: self.get_temp(),
            AOD_TIMESTAMP_LOCAL: self.get_timestamp_local(),
            AOD_TIMESTAMP_UTC: self.get_timestamp_utc(),
            AOD_WIND_DIRECTION: self.get_wind_direction(),
            AOD_WIND_SPEED: self.get_wind_speed(),
            AOD_WIND_SPEED_MAX: self.get_wind_speed_max(),
        }

        return data

    def parse_interval_value(
        self, values: Any, hour: int, key: str = AEMET_ATTR_VALUE
    ) -> Any:
        """Parse Town hourly forecast interval value from data."""
        period_offset = None

        for value in values:
            if key not in value:
                continue
            period = value[AEMET_ATTR_PERIOD]
            period_start = int(period[0:API_PERIOD_SPLIT])
            period_end = int(period[API_PERIOD_SPLIT : API_PERIOD_SPLIT * 2])
            if period_end < period_start:
                if period_offset is None or period_end < period_offset:
                    period_offset = period_end

        if period_offset is None:
            period_offset = 0

        for value in values:
            if key not in value:
                continue
            period = value[AEMET_ATTR_PERIOD]
            period_start = int(period[0:API_PERIOD_SPLIT])
            period_end = int(period[API_PERIOD_SPLIT : API_PERIOD_SPLIT * 2])
            period_start -= period_offset
            period_end -= period_offset
            if period_end < period_start:
                period_end = period_end + API_PERIOD_24H
                if hour == 0:
                    hour = hour + API_PERIOD_24H
            if period_start <= hour < period_end:
                return None if not value[key] else value[key]

        return None

    def parse_value(self, values: Any, hour: int, key: str = AEMET_ATTR_VALUE) -> Any:
        """Parse Town hourly forecast value from data."""
        for value in values:
            if key not in value:
                continue
            if int(value[AEMET_ATTR_PERIOD]) == hour:
                return None if not value[key] else value[key]
        return None
