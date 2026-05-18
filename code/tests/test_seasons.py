"""Tests for season lookup and comparison."""

import unittest

from season_tool.seasons import (
    compare_country_seasons,
    format_traditional_season,
    get_meteorological_season,
    get_traditional_season,
)
from season_tool.validation import InvalidCountryError, InvalidMonthError


class SeasonLookupTests(unittest.TestCase):
    def test_australia_meteorological_seasons(self):
        cases = {
            "January": "Summer",
            "April": "Autumn",
            "July": "Winter",
            "October": "Spring",
        }
        for month, expected in cases.items():
            with self.subTest(month=month):
                self.assertEqual(get_meteorological_season("Australia", month), expected)

    def test_northern_countries_share_meteorological_calendar(self):
        self.assertEqual(get_meteorological_season("Spain", "March"), "Spring")
        self.assertEqual(get_meteorological_season("Japan", 8), "Summer")

    def test_mauritius_custom_meteorological_calendar(self):
        self.assertEqual(get_meteorological_season("Mauritius", "November"), "Summer")
        self.assertEqual(get_meteorological_season("Mauritius", "May"), "Autumn")
        self.assertEqual(get_meteorological_season("Mauritius", "September"), "Winter")
        self.assertEqual(get_meteorological_season("Mauritius", "October"), "Spring")

    def test_malaysia_and_sri_lanka_monsoon_calendar(self):
        self.assertEqual(get_meteorological_season("Malaysia", "February"), "Northeast Monsoon")
        self.assertEqual(get_meteorological_season("Sri Lanka", "March"), "Inter-monsoon")
        self.assertEqual(get_meteorological_season("Malaysia", "July"), "Southeast Monsoon")
        self.assertEqual(get_meteorological_season("Sri Lanka", "November"), "Inter-monsoon")

    def test_australia_traditional_noongar_season(self):
        self.assertEqual(get_traditional_season("Australia", "August"), "Djilba")
        self.assertIn("Djilba", format_traditional_season("Australia", "August"))

    def test_country_without_traditional_calendar_returns_none(self):
        self.assertIsNone(get_traditional_season("Spain", "January"))
        with self.assertRaisesRegex(ValueError, "only available for Australia"):
            format_traditional_season("Spain", "January")

    def test_compare_same_meteorological_season(self):
        comparison = compare_country_seasons("Malaysia", "Sri Lanka", "July")
        self.assertTrue(comparison.same)
        self.assertEqual(comparison.country_one_season, "Southeast Monsoon")

    def test_compare_different_meteorological_season(self):
        comparison = compare_country_seasons("Australia", "Japan", "January")
        self.assertFalse(comparison.same)
        self.assertEqual(comparison.country_one_season, "Summer")
        self.assertEqual(comparison.country_two_season, "Winter")

    def test_unsupported_country_is_rejected(self):
        with self.assertRaises(InvalidCountryError):
            get_meteorological_season("Canada", "March")

    def test_invalid_month_boundaries(self):
        for month in (0, 13):
            with self.subTest(month=month):
                with self.assertRaises(InvalidMonthError):
                    get_meteorological_season("Australia", month)


if __name__ == "__main__":
    unittest.main()
