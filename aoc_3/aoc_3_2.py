"""If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced."""

from collections import defaultdict

GEAR_NUMBERS = defaultdict(list)


def read_puzzle():
    with open("input.txt", "r") as f:
        # with open("small_input.txt", "r") as f:
        return f.read().splitlines()


def solve_puzzle(puzzle):
    result = 0
    for i, line in enumerate(puzzle):
        find_gear_numbers(line, puzzle, i)
    for gear_numbers in GEAR_NUMBERS.values():
        if len(gear_numbers) == 2:
            result += gear_numbers[0] * gear_numbers[1]
    return result


def find_gear_numbers(line, puzzle, i):
    adjacent_stars = []
    number = 0
    for j, char in enumerate(line):
        if char.isdigit():
            number = number * 10 + int(char)
            adjacent_stars.extend(get_adjacent_stars(puzzle, i, j))
        else:
            for gear_location in set(adjacent_stars):
                GEAR_NUMBERS[gear_location].append(number)
            adjacent_stars = []
            number = 0

    else:
        for gear_location in set(adjacent_stars):
            GEAR_NUMBERS[gear_location].append(number)


def get_adjacent_stars(puzzle, i, j):
    fields_to_check = [
        (i - 1, j - 1),
        (i - 1, j),
        (i - 1, j + 1),
        (i, j - 1),
        (i, j + 1),
        (i + 1, j - 1),
        (i + 1, j),
        (i + 1, j + 1),
    ]
    adjacent_stars = []
    for field in fields_to_check:
        if (
            field[0] >= 0
            and field[1] >= 0
            and field[0] < len(puzzle)
            and field[1] < len(puzzle[0])
        ):
            if check_field(field, puzzle):
                adjacent_stars.append(field)
    return adjacent_stars


def check_field(field, puzzle):
    i, j = field
    check = puzzle[i][j] == "*"
    print(f"Checking {i} {j} -> {puzzle[i][j]} is {check}")
    return check


if __name__ == "__main__":
    puzzle = read_puzzle()
    print(solve_puzzle(puzzle))
