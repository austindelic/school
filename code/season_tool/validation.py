"""Validation helpers."""

from __future__ import annotations

import re
from typing import Any, Mapping

from season_tool.data import (
    CITY_ALIASES,
    CITY_TEMPERATURE_DATA,
    COUNTRY_ALIASES,
    COUNTRY_SEASON_DATA,
    MONTH_LOOKUP,
)


class ValidationError(ValueError):
    """Base class for user input validation errors."""


class InvalidCountryError(ValidationError):
    """Raised when a country is not supported by the tool."""


class InvalidMonthError(ValidationError):
    """Raised when a month is outside the accepted month values."""


class InvalidCityError(ValidationError):
    """Raised when a city is not supported by the tool."""


class InvalidTemperatureError(ValidationError):
    """Raised when a temperature is not numeric or outside a city range."""


class InvalidPeriodError(ValidationError):
    """Raised when a period is not supported."""


TEMPERATURE_PATTERN = re.compile(r"^-?\d+(?:\.\d)?$")


def _lookup_alias(
    value: str,
    aliases: Mapping[str, str],
    valid_values: Mapping[str, object],
    field_name: str,
    plural_name: str,
    error_type: type[ValidationError],
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise error_type(f"{field_name} must be a non-empty string.")

    key = " ".join(value.strip().lower().split())
    if key not in aliases:
        valid = ", ".join(valid_values)
        raise error_type(
            f"Unsupported {field_name.lower()} '{value}'. "
            f"Supported {plural_name}: {valid}."
        )
    return aliases[key]


def normalize_country(country: str) -> str:
    """Return the canonical country name for a supported country."""

    return _lookup_alias(
        country,
        COUNTRY_ALIASES,
        COUNTRY_SEASON_DATA,
        "Country",
        "countries",
        InvalidCountryError,
    )


def parse_month(month: Any) -> int:
    """Convert a month number or month name to an integer from 1 to 12."""

    if isinstance(month, bool):
        raise InvalidMonthError("Month must be a name or number from 1 to 12.")

    if isinstance(month, int):
        month_number = month
    elif isinstance(month, str):
        cleaned = month.strip()
        if cleaned.isdigit():
            month_number = int(cleaned)
        else:
            lookup_key = cleaned.lower()
            if lookup_key not in MONTH_LOOKUP:
                raise InvalidMonthError(
                    f"Invalid month '{month}'. Use a month name or number from 1 to 12."
                )
            month_number = MONTH_LOOKUP[lookup_key]
    else:
        raise InvalidMonthError("Month must be a name or number from 1 to 12.")

    if month_number < 1 or month_number > 12:
        raise InvalidMonthError("Month number must be between 1 and 12.")
    return month_number


def normalize_city(city: str) -> str:
    """Return the canonical city name for a supported city."""

    return _lookup_alias(
        city,
        CITY_ALIASES,
        CITY_TEMPERATURE_DATA,
        "City",
        "cities",
        InvalidCityError,
    )


def normalize_period(period: str) -> str:
    """Return morning or afternoon."""

    if not isinstance(period, str) or not period.strip():
        raise InvalidPeriodError("Period must be morning, evening, afternoon, or 3pm.")

    key = period.strip().lower()
    if key == "morning":
        return "morning"
    if key in {"evening", "afternoon", "3pm", "3 pm"}:
        return "afternoon"
    raise InvalidPeriodError("Period must be morning, evening, afternoon, or 3pm.")


def parse_temperature(temperature: Any) -> float:
    """Convert a one-decimal temperature value to float."""

    if isinstance(temperature, bool):
        raise InvalidTemperatureError("Temperature must be a numeric value.")

    if isinstance(temperature, (int, float)):
        value = float(temperature)
        if abs(value - round(value, 1)) > 0.000001:
            raise InvalidTemperatureError(
                "Temperature must be accurate to one decimal place."
            )
        return value

    if isinstance(temperature, str):
        cleaned = temperature.strip()
        if not TEMPERATURE_PATTERN.fullmatch(cleaned):
            raise InvalidTemperatureError(
                "Temperature must be numeric and use at most one decimal place."
            )
        try:
            return float(cleaned)
        except ValueError as exc:
            raise InvalidTemperatureError(
                f"Temperature '{temperature}' is not numeric."
            ) from exc

    raise InvalidTemperatureError("Temperature must be a numeric value.")


def validate_temperature_for_city(city: str, temperature: float) -> None:
    """Validate that the temperature is inside the city range."""

    profile = CITY_TEMPERATURE_DATA[city]
    if temperature < profile.minimum_valid or temperature > profile.maximum_valid:
        raise InvalidTemperatureError(
            f"Temperature {temperature:.1f}C is outside the valid range for {city} "
            f"({profile.minimum_valid:.1f}C to {profile.maximum_valid:.1f}C)."
        )
