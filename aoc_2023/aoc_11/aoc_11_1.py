import inspect
from collections import Counter
from functools import cmp_to_key
from typing import Dict, Set, Tuple

from util.process_input import Puzzle, read_puzzle, string_of_numbers_to_list

Galaxy = list[str]
star = "#"
void = "."


def solve_puzzle(puzzle: Puzzle) -> int:
    galaxy: Galaxy = puzzle
    galaxy = expand_galaxy(galaxy)
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
    for i in range(len(stars) - 1):
        for j in range(i + 1, len(stars)):
            path_lengths.append(
                get_shortest_path_length_between_stars(stars[i], stars[j])
            )
            print(f"({i} - {j})\t{path_lengths[-1]}")
    return path_lengths


def get_stars(galaxy: Galaxy) -> list[tuple[int, int]]:
    stars = []
    for i, row in enumerate(galaxy):
        for j, cell in enumerate(row):
            if cell == star:
                stars.append((i, j))
    return stars


def get_shortest_path_length_between_stars(star1: tuple[int], star2: tuple[int]) -> int:
    """Manhattan distance between two stars"""
    distance = abs(star1[0] - star2[0]) + abs(star1[1] - star2[1])
    # print(distance)
    return distance


if __name__ == "__main__":
    SMALL = True
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
