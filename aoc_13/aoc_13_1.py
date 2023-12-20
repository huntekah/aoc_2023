import inspect
import re
from collections import defaultdict
from functools import cache
from itertools import product

from tqdm import tqdm

# from util.process_input import Puzzle, read_puzzle, string_of_numbers_to_list
from util.process_input import Puzzle, string_of_numbers_to_list

### Puzzle description ###
# find mirror reflections of text input, either row or column wise:
# 123456789
#     ><
# #.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.
#     ><
# 123456789
#
# or
# 1 #...##..# 1
# 2 #....#..# 2
# 3 ..##..### 3
# 4v#####.##.v4
# 5^#####.##.^5
# 6 ..##..### 6
# 7 #....#..# 7
### PUZZLE DESCRIPTION END ###

Pattern = list[str]
Patterns = list[Pattern]


def solve_puzzle(puzzle: Patterns) -> int:
    records: Patterns = puzzle

    row_mirrors = 0
    column_mirrors = 0
    for record in records:
        print("\n".join(record))
        hashed_rows = get_hashed_rows(record)
        hashed_columns = get_hashed_columns(record)
        if mirror_location := find_mirror_location(hashed_rows):
            row_mirrors += mirror_location
            print(f"ROW MIRROR FOUND AT {mirror_location}")
        elif mirror_location := find_mirror_location(hashed_columns):
            column_mirrors += mirror_location
            print(f"COLUMN MIRROR FOUND AT {mirror_location}")
        print("______________________")
    print(f"{row_mirrors=} {column_mirrors=}")
    return 100 * row_mirrors + column_mirrors


def get_hashed_rows(record: Pattern) -> dict[int, list[int]]:
    hashed_rows = defaultdict(list)
    for i, row in enumerate(record, 1):
        hashed_rows[hash(row)].append(i)
    return hashed_rows


def get_hashed_columns(record: Pattern) -> dict[int, list[int]]:
    hashed_columns = defaultdict(list)
    for i, column in enumerate(zip(*record), 1):
        hashed_columns[hash(column)].append(i)
    return hashed_columns


def find_mirror_location(hashed_rows: dict[int, list[int]]) -> int:
    # find all middles
    # for all middles, make a list of tuples of all matching row indices, if it would be a mirror
    # iterate through hashed_rows, and delete tuple from middles_list, if it is in there
    # if middles_list is empty, we found a mirror
    middles_list = []

    for row_hash, row_indices in hashed_rows.items():
        possible_mirrors_middles = [
            (row_indices[i], row_indices[i + 1])
            for i in range(len(row_indices) - 1)
            if abs(row_indices[i] - row_indices[i + 1]) == 1
        ]
        middles_list.extend(possible_mirrors_middles)

    print(hashed_rows.values())
    last_row = max(
        row_id for row_indices in hashed_rows.values() for row_id in row_indices
    )
    for try_middle in middles_list:
        a = try_middle[0]
        b = try_middle[1]
        is_middle = False
        while a >= 1 and b <= last_row:
            is_middle = False
            for row_indices in hashed_rows.values():
                if a in row_indices and b in row_indices:
                    is_middle = True
                    break
            if not is_middle:
                break
            a -= 1
            b += 1
        if is_middle:
            print(try_middle)
            return try_middle[0]

    return None


def read_puzzle(filename: str) -> Patterns:
    with open(filename) as file:
        records = [
            pattern.strip().split("\n") for pattern in file.read().strip().split("\n\n")
        ]
        return records


if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle: Patterns = read_puzzle("small_input2.txt")
        result = solve_puzzle(puzzle)
        print(result)
        assert 709 == result
    else:
        puzzle = read_puzzle("input.txt")
        print(solve_puzzle(puzzle))
