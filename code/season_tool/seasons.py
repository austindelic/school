"""Season lookup and comparison."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from season_tool.data import COUNTRY_SEASON_DATA, MONTH_NAMES
from season_tool.validation import normalize_country, parse_month


@dataclass(frozen=True)
class SeasonComparison:
    """Country season comparison result."""

    country_one: str
    country_two: str
    month: str
    country_one_season: str
    country_two_season: str
    same: bool
    message: str


def get_meteorological_season(country: str, month: object) -> str:
    """Return a meteorological season."""

    country_name = normalize_country(country)
    month_number = parse_month(month)
    return COUNTRY_SEASON_DATA[country_name].meteorological[month_number]


def format_meteorological_season(country: str, month: object) -> str:
    """Return a meteorological season message."""

    country_name = normalize_country(country)
    month_number = parse_month(month)
    season = COUNTRY_SEASON_DATA[country_name].meteorological[month_number]
    month_name = MONTH_NAMES[month_number]
    return f"The meteorological season in {country_name} in {month_name} is {season}."


def get_traditional_season(country: str, month: object) -> Optional[str]:
    """Return a traditional season if one is recorded."""

    country_name = normalize_country(country)
    month_number = parse_month(month)
    calendar = COUNTRY_SEASON_DATA[country_name].traditional
    if calendar is None:
        return None
    return calendar[month_number]


def format_traditional_season(country: str, month: object) -> str:
    """Return a traditional season message."""

    country_name = normalize_country(country)
    if country_name != "Australia":
        raise ValueError("Traditional season data is only available for Australia.")

    month_number = parse_month(month)
    season = get_traditional_season(country_name, month_number)
    month_name = MONTH_NAMES[month_number]
    return f"The traditional season in {country_name} in {month_name} is {season}."


def compare_country_seasons(
    country_one: str,
    country_two: str,
    month: object,
) -> SeasonComparison:
    """Compare two countries' meteorological seasons for one month."""

    first_country = normalize_country(country_one)
    second_country = normalize_country(country_two)
    month_number = parse_month(month)
    month_name = MONTH_NAMES[month_number]
    first_season = COUNTRY_SEASON_DATA[first_country].meteorological[month_number]
    second_season = COUNTRY_SEASON_DATA[second_country].meteorological[month_number]
    same = first_season == second_season

    if same:
        message = (
            f"{first_country} and {second_country} have the same meteorological "
            f"season in {month_name}: {first_season}."
        )
    else:
        message = (
            f"{first_country} and {second_country} have different meteorological "
            f"seasons in {month_name}: {first_country} has {first_season}, "
            f"{second_country} has {second_season}."
        )

    return SeasonComparison(
        country_one=first_country,
        country_two=second_country,
        month=month_name,
        country_one_season=first_season,
        country_two_season=second_season,
        same=same,
        message=message,
    )
