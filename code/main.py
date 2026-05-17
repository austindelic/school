"""Command-line interface for the seasons and temperature tool."""

from __future__ import annotations

import argparse

from season_tool.io_handlers import process_request_file
from season_tool.seasons import (
    compare_country_seasons,
    format_traditional_season,
    get_meteorological_season,
)
from season_tool.temperature import compare_with_city_average, compare_with_perth_average
from season_tool.validation import ValidationError


def run_demo() -> None:
    """Print the demo output."""

    print("Season and temperature learning tool demo")
    print("-" * 43)
    print(f"Australia in January: {get_meteorological_season('Australia', 'January')}")
    print(format_traditional_season("Australia", "August"))
    print(compare_country_seasons("Australia", "Japan", "January").message)
    print(compare_with_city_average("Perth", 29.0, "evening").message)
    print(compare_with_perth_average("Brisbane", 31.0, "morning").message)


def run_interactive() -> None:
    """Read keyboard requests until the user chooses to stop."""

    while True:
        print("Choose an option:")
        print("1. Find meteorological season")
        print("2. Find Australia Noongar season")
        print("3. Compare country seasons")
        print("4. Compare city temperature average")
        print("5. Compare reading with Perth average")
        choice = input("Enter option number: ").strip()

        try:
            if choice == "1":
                country = input("Country: ")
                month = input("Month: ")
                print(get_meteorological_season(country, month))
            elif choice == "2":
                month = input("Month: ")
                print(format_traditional_season("Australia", month))
            elif choice == "3":
                first_country = input("First country: ")
                second_country = input("Second country: ")
                month = input("Month: ")
                print(
                    compare_country_seasons(first_country, second_country, month).message
                )
            elif choice == "4":
                city = input("City: ")
                period = input("Period (morning/evening/afternoon/3pm): ")
                temperature = input("Temperature reading: ")
                print(compare_with_city_average(city, temperature, period).message)
            elif choice == "5":
                city = input("City: ")
                period = input("Period (morning/evening/afternoon/3pm): ")
                temperature = input("Temperature reading: ")
                print(compare_with_perth_average(city, temperature, period).message)
            else:
                print("Unknown option.")
        except (ValidationError, ValueError) as exc:
            print(f"Error: {exc}")

        answer = input("Do you want to ask something else? (y/n): ").strip().lower()
        if answer not in {"y", "yes"}:
            break


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find seasons and compare weather readings."
    )
    parser.add_argument("--demo", action="store_true", help="print the demo output")
    parser.add_argument(
        "--file",
        nargs=2,
        metavar=("INPUT", "OUTPUT"),
        help="process CSV-style request file and write results",
    )
    args = parser.parse_args()

    if args.demo:
        run_demo()
    elif args.file:
        processed = process_request_file(args.file[0], args.file[1])
        print(f"Processed {processed} request lines.")
    else:
        run_interactive()


if __name__ == "__main__":
    main()
