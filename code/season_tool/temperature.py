"""Temperature comparisons."""

from __future__ import annotations

from dataclasses import dataclass

from season_tool.data import CITY_TEMPERATURE_DATA
from season_tool.validation import (
    normalize_city,
    normalize_period,
    parse_temperature,
    validate_temperature_for_city,
)

SIGNIFICANT_DIFFERENCE_C = 6.0
SAME_TOLERANCE_C = 0.01


@dataclass(frozen=True)
class TemperatureComparison:
    """Temperature comparison result."""

    city: str
    period: str
    reading: float
    average: float
    relation: str
    difference: float
    significant_difference: bool
    message: str


def _validated_reading(city: str, temperature: object, period: str) -> tuple[str, str, float]:
    city_name = normalize_city(city)
    period_name = normalize_period(period)
    reading = parse_temperature(temperature)
    validate_temperature_for_city(city_name, reading)
    return city_name, period_name, reading


def _build_comparison(
    city: str, period: str, reading: float, average: float
) -> TemperatureComparison:
    difference = reading - average
    absolute_difference = abs(difference)

    if absolute_difference <= SAME_TOLERANCE_C:
        relation = "same"
        relation_text = "the same as"
    elif difference > 0:
        relation = "above"
        relation_text = "above"
    else:
        relation = "below"
        relation_text = "below"

    significant = absolute_difference > SIGNIFICANT_DIFFERENCE_C
    message = (
        f"{reading:.1f}C is {relation_text} {city}'s {period} average "
        f"of {average:.1f}C by {absolute_difference:.1f}C."
    )
    if significant:
        message += " The difference is more than 6.0C."

    return TemperatureComparison(
        city=city,
        period=period,
        reading=reading,
        average=average,
        relation=relation,
        difference=absolute_difference,
        significant_difference=significant,
        message=message,
    )


def compare_with_city_average(city: str, temperature: object, period: str) -> TemperatureComparison:
    """Compare a reading with a city average."""

    city_name, period_name, reading = _validated_reading(city, temperature, period)
    average = CITY_TEMPERATURE_DATA[city_name].averages[period_name]
    return _build_comparison(city_name, period_name, reading, average)


def compare_with_perth_average(city: str, temperature: object, period: str) -> TemperatureComparison:
    """Compare a reading with Perth's average."""

    _source_city, period_name, reading = _validated_reading(city, temperature, period)
    perth_average = CITY_TEMPERATURE_DATA["Perth"].averages[period_name]
    return _build_comparison("Perth", period_name, reading, perth_average)
