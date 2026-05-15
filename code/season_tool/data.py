"""Data from the assignment figures."""

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Optional


@dataclass(frozen=True)
class CountrySeasonProfile:
    """Season calendars for one country."""

    meteorological: Mapping[int, str]
    traditional: Optional[Mapping[int, str]] = None


@dataclass(frozen=True)
class CityTemperatureProfile:
    """Average temperatures and valid input range for one city."""

    averages: Mapping[str, float]
    minimum_valid: float
    maximum_valid: float


MONTH_NAMES: Mapping[int, str] = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}

MONTH_LOOKUP: Dict[str, int] = {
    name.lower(): number for number, name in MONTH_NAMES.items()
}

MONTH_LOOKUP.update(
    {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "sept": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
    }
)


def _calendar(entries: Mapping[str, Iterable[int]]) -> Dict[int, str]:
    calendar: Dict[int, str] = {}
    for season, months in entries.items():
        for month in months:
            calendar[month] = season
    return calendar


NORTHERN_METEOROLOGICAL = _calendar(
    {
        "Winter": (12, 1, 2),
        "Spring": range(3, 6),
        "Summer": range(6, 9),
        "Autumn": range(9, 12),
    }
)

SOUTHERN_METEOROLOGICAL = _calendar(
    {
        "Summer": (12, 1, 2),
        "Autumn": range(3, 6),
        "Winter": range(6, 9),
        "Spring": range(9, 12),
    }
)

MAURITIUS_METEOROLOGICAL = _calendar(
    {
        "Summer": (11, 12, 1, 2, 3, 4),
        "Autumn": (5,),
        "Winter": range(6, 10),
        "Spring": (10,),
    }
)

MALAYSIA_SRI_LANKA_METEOROLOGICAL = _calendar(
    {
        "Northeast Monsoon": (12, 1, 2),
        "Inter-monsoon": (3, 4, 10, 11),
        "Southeast Monsoon": range(5, 10),
    }
)

AUSTRALIA_TRADITIONAL = _calendar(
    {
        "Birak": (12, 1),
        "Bunuru": range(2, 4),
        "Djeran": range(4, 6),
        "Makuru": range(6, 8),
        "Djilba": range(8, 10),
        "Kambarang": range(10, 12),
    }
)

COUNTRY_SEASON_DATA: Mapping[str, CountrySeasonProfile] = {
    "Australia": CountrySeasonProfile(
        meteorological=SOUTHERN_METEOROLOGICAL,
        traditional=AUSTRALIA_TRADITIONAL,
    ),
    "Spain": CountrySeasonProfile(
        meteorological=NORTHERN_METEOROLOGICAL,
        traditional=None,
    ),
    "Japan": CountrySeasonProfile(
        meteorological=NORTHERN_METEOROLOGICAL,
        traditional=None,
    ),
    "Mauritius": CountrySeasonProfile(
        meteorological=MAURITIUS_METEOROLOGICAL,
        traditional=None,
    ),
    "Malaysia": CountrySeasonProfile(
        meteorological=MALAYSIA_SRI_LANKA_METEOROLOGICAL,
        traditional=None,
    ),
    "Sri Lanka": CountrySeasonProfile(
        meteorological=MALAYSIA_SRI_LANKA_METEOROLOGICAL,
        traditional=None,
    ),
}

COUNTRY_ALIASES: Mapping[str, str] = {
    "australia": "Australia",
    "spain": "Spain",
    "japan": "Japan",
    "mauritius": "Mauritius",
    "malaysia": "Malaysia",
    "sri lanka": "Sri Lanka",
    "srilanka": "Sri Lanka",
}

CITY_TEMPERATURE_DATA: Mapping[str, CityTemperatureProfile] = {
    "Perth": CityTemperatureProfile(
        averages={"morning": 18.2, "afternoon": 23.0},
        minimum_valid=0.7,
        maximum_valid=46.0,
    ),
    "Adelaide": CityTemperatureProfile(
        averages={"morning": 16.5, "afternoon": 21.0},
        minimum_valid=-1.0,
        maximum_valid=49.0,
    ),
    "Brisbane": CityTemperatureProfile(
        averages={"morning": 21.8, "afternoon": 24.8},
        minimum_valid=2.6,
        maximum_valid=41.7,
    ),
}

CITY_ALIASES: Mapping[str, str] = {
    "perth": "Perth",
    "adelaide": "Adelaide",
    "brisbane": "Brisbane",
}
