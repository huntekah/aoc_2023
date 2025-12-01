#!/usr/bin/env python3
"""
Script to download Advent of Code input data.
Usage: python util/get_data.py <day>
"""

import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv


def get_input_data(day: int, year: int = 2025) -> str:
    """Download input data for a specific day."""
    load_dotenv()

    session_cookie = os.getenv("AOC_SESSION")
    if not session_cookie:
        raise ValueError(
            "AOC_SESSION not found in .env file. "
            "Please add your session cookie from adventofcode.com"
        )

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    cookies = {"session": session_cookie}

    response = requests.get(url, cookies=cookies)
    response.raise_for_status()

    return response.text


def save_input(day: int, data: str) -> None:
    """Save input data to the appropriate directory."""
    day_dir = Path(f"aoc_{day}")
    day_dir.mkdir(exist_ok=True)

    input_file = day_dir / "input.txt"
    input_file.write_text(data)

    print(f"✓ Input data saved to {input_file}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python util/get_data.py <day>")
        sys.exit(1)

    try:
        day = int(sys.argv[1])
        if not 1 <= day <= 25:
            raise ValueError("Day must be between 1 and 25")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        print(f"Downloading input for day {day}...")
        data = get_input_data(day)
        save_input(day, data)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Error: Input for day {day} not available yet")
        else:
            print(f"HTTP Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
