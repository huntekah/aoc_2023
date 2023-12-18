import inspect
from collections import Counter
from functools import cmp_to_key
from typing import Dict, Set, Tuple
from tqdm import tqdm

from util.process_input import Puzzle, read_puzzle, string_of_numbers_to_list

Galaxy = list[str]
star = "#"
void = "."


def solve_puzzle(puzzle: Puzzle) -> int:
    galaxy: Galaxy = puzzle
    # galaxy = expand_galaxy(galaxy)
    path_lengths: list[int] = get_shortest_path_lengths_between_stars(galaxy)
    return sum(path_lengths)


def expand_galaxy(galaxy: Galaxy) -> Galaxy:
    """Expands each row / column to be twice as bigm if they contain no stars"""
    new_galaxy = []
    # expand rows
    for row in galaxy:
        if star not in row:
            new_galaxy.append(row)
        new_galaxy.append(row)
    galaxy = new_galaxy
    new_galaxy_T = []
    # expand columns
    for column in zip(*galaxy):
        if star not in column:
            new_galaxy_T.append("".join(column))
        new_galaxy_T.append(column)
    galaxy = ["".join(row) for row in zip(*new_galaxy_T)]
    return galaxy


def get_shortest_path_lengths_between_stars(galaxy: Galaxy) -> list[int]:
    stars: list[tuple[int, int]] = get_stars(galaxy)
    path_lengths = []
    # print("->",get_shortest_path_length_between_stars(galaxy, stars[1], stars[2]))
    # return [-1]
    # count overall progress with tqdm
    for i in tqdm(range(len(stars) - 1)):
        for j in range(i + 1, len(stars)):
            path_lengths.append(
                get_shortest_path_length_between_stars(galaxy, stars[i], stars[j])
            )
            # print(f"({i} - {j})\t{path_lengths[-1]}")
    return path_lengths


def get_stars(galaxy: Galaxy) -> list[tuple[int, int]]:
    stars = []
    for i, row in enumerate(galaxy):
        for j, cell in enumerate(row):
            if cell == star:
                stars.append((i, j))
    # print("\n".join([f"{i}\t({s[0]},{s[1]})" for i,s in enumerate(stars)]))
    return stars


def get_shortest_path_length_between_stars(
    galaxy: Galaxy, star1: tuple[int, int], star2: tuple[int, int]
) -> int:
    """Manhattan distance between two stars"""
    void_multiplier = 1000000
    empty_rows = count_empty_rows_between_stars(galaxy, star1, star2)
    empty_columns = count_empty_columns_between_stars(galaxy, star1, star2)
    # empty_crossings = count_empty_crossings_between_stars(galaxy, star1, star2)
    # print(f"{empty_rows=} {empty_columns=}")
    additional_steps = (empty_rows + empty_columns) * (void_multiplier - 1) #+ empty_crossings * (void_multiplier - 1) ** 2
    # additional_rows = empty_rows * (void_multiplier)
    # additional_columns = empty_columns * (void_multiplier)
    # print(f"{additional_steps=}")
    # print(f"{empty_rows=} {empty_columns=}")
    # print(f" regular rows = {abs(star1[0] - star2[0])}")
    # print(f" regular columns = {abs(star1[1] - star2[1])}")
    distance = (
        abs(star1[0] - star2[0])
        + abs(star1[1] - star2[1])
        + additional_steps
    )

    return distance


def count_empty_rows_between_stars(
    galaxy: Galaxy, star1: tuple[int, int], star2: tuple[int, int]
) -> int:
    empty_rows = 0
    first_row = min(star1[0], star2[0])
    last_row = max(star1[0], star2[0])
    for i in range(first_row, last_row):
        if is_empty_row(galaxy, i):
            # print(galaxy[i])
            empty_rows += 1
    return empty_rows


def count_empty_columns_between_stars(
    galaxy: Galaxy, star1: tuple[int, int], star2: tuple[int, int]
) -> int:
    empty_columns = 0
    first_column = min(star1[1], star2[1])
    last_column = max(star1[1], star2[1])
    for i in range(first_column, last_column):
        if is_empty_column(galaxy, i):
            empty_columns += 1
    return empty_columns


def is_empty_row(galaxy: Galaxy, row: int) -> bool:
    return star not in galaxy[row]

def is_empty_column(galaxy: Galaxy, column: int) -> bool:
    return star not in list(zip(*galaxy))[column]
def count_empty_crossings_between_stars(
    galaxy: Galaxy, star1: tuple[int, int], star2: tuple[int, int]
) -> int:
    empty_crossings = 0
    for i in range(star1[0], star2[0]):
        for j in range(star1[1], star2[1]):
            if is_empty_column(galaxy, j) and is_empty_row(galaxy, i):
                empty_crossings += 1
    return empty_crossings


if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle: Puzzle = read_puzzle("small_input.txt")
        result = solve_puzzle(puzzle)
        print(result)
        assert 374 == result
    else:
        puzzle = read_puzzle("input.txt")
        print(solve_puzzle(puzzle))


# ....1........
# .........2...
# 3............
# .............
# .............
# ........4....
# .5...........
# .#..........6
# .#...........
# .#...........
# .####....7...
# 8....9.......
