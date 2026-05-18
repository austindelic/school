"""Tests for temperature comparison."""

import unittest

from season_tool.data import CITY_TEMPERATURE_DATA
from season_tool.temperature import (
    SIGNIFICANT_DIFFERENCE_C,
    compare_with_city_average,
    compare_with_perth_average,
)
from season_tool.validation import (
    InvalidCityError,
    InvalidPeriodError,
    InvalidTemperatureError,
)


class TemperatureComparisonTests(unittest.TestCase):
    def test_same_as_average(self):
        result = compare_with_city_average("Perth", "23.0", "evening")
        self.assertEqual(result.relation, "same")
        self.assertFalse(result.significant_difference)

    def test_below_average(self):
        result = compare_with_city_average("Adelaide", "20.0", "evening")
        self.assertEqual(result.relation, "below")
        self.assertAlmostEqual(result.difference, 1.0)

    def test_above_average_with_large_difference(self):
        result = compare_with_city_average("Brisbane", "31.0", "morning")
        self.assertEqual(result.relation, "above")
        self.assertGreater(result.difference, SIGNIFICANT_DIFFERENCE_C)
        self.assertTrue(result.significant_difference)

    def test_difference_of_exactly_six_is_not_large(self):
        result = compare_with_city_average("Perth", "29.0", "evening")
        self.assertAlmostEqual(result.difference, 6.0)
        self.assertFalse(result.significant_difference)

    def test_evening_and_3pm_map_to_afternoon_average(self):
        afternoon = compare_with_city_average("Brisbane", "24.8", "afternoon")
        three_pm = compare_with_city_average("Brisbane", "24.8", "3pm")
        evening = compare_with_city_average("Brisbane", "24.8", "evening")
        self.assertEqual(afternoon.period, "afternoon")
        self.assertEqual(three_pm.relation, "same")
        self.assertEqual(evening.period, "afternoon")

    def test_selected_city_profiles_are_limited_to_three_cities(self):
        self.assertEqual(
            set(CITY_TEMPERATURE_DATA),
            {"Perth", "Adelaide", "Brisbane"},
        )

    def test_minimum_and_maximum_city_boundaries_are_valid(self):
        self.assertEqual(compare_with_city_average("Perth", "0.7", "morning").relation, "below")
        self.assertEqual(compare_with_city_average("Perth", "46.0", "evening").relation, "above")

    def test_outside_city_range_is_invalid(self):
        for value in ("0.6", "46.1"):
            with self.subTest(value=value):
                with self.assertRaises(InvalidTemperatureError):
                    compare_with_city_average("Perth", value, "morning")

    def test_last_three_student_id_digits_temperature_is_invalid_for_adelaide(self):
        with self.assertRaises(InvalidTemperatureError):
            compare_with_city_average("Adelaide", "121", "morning")

    def test_temperature_with_two_decimal_places_is_invalid(self):
        with self.assertRaises(InvalidTemperatureError):
            compare_with_city_average("Perth", "18.25", "morning")

    def test_boolean_temperature_is_invalid(self):
        with self.assertRaises(InvalidTemperatureError):
            compare_with_city_average("Perth", True, "morning")

    def test_invalid_city(self):
        with self.assertRaises(InvalidCityError):
            compare_with_city_average("Melbourne", "20.0", "morning")

    def test_invalid_period(self):
        with self.assertRaises(InvalidPeriodError):
            compare_with_city_average("Perth", "20.0", "night")

    def test_compare_reading_with_perth_average(self):
        result = compare_with_perth_average("Brisbane", "31.0", "morning")
        self.assertEqual(result.city, "Perth")
        self.assertEqual(result.relation, "above")
        self.assertTrue(result.significant_difference)


if __name__ == "__main__":
    unittest.main()
