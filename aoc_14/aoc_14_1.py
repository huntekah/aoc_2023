import inspect
import re
from functools import cache
from itertools import product

from tqdm import tqdm

from util.process_input import Puzzle, read_puzzle, string_of_numbers_to_list

### Puzzle description ###

### PUZZLE DESCRIPTION END ###

Record = list[str]


def solve_puzzle(puzzle: Puzzle) -> int:
    record: Record = puzzle
    # r1 = rotate_90_clockwise(record)
    r3 = rotate_90_counter_clokwise(record)
    slided_up = rotate_90_clockwise(slide_stones_left(r3))

    # print("\n".join(record))
    # print("_")
    # print("\n".join(slided_up))
    # print("_")
    # print("\n".join(r1))
    return count_stones_weight(slided_up)


def rotate_90_clockwise(record: Record) -> Record:
    # return ["".join(x) for x in list(zip(*record[::-1]))]
    return rotate_90_counter_clokwise(
        rotate_90_counter_clokwise(rotate_90_counter_clokwise(record))
    )


def rotate_90_counter_clokwise(record: Record) -> Record:
    return ["".join(x) for x in list(zip(*record))]


def slide_stones_left(record: Record) -> Record:
    # for symbols .#O, move each O to the rightmost position, if it is not blocked by #
    stone = "O"
    block = "#"
    empty = "."
    new_record = []
    for row in record:
        new_row = []
        stones = []
        emptys = []
        for i, symbol in enumerate(row):
            if symbol == stone:
                stones.append(stone)
            elif symbol == empty:
                emptys.append(empty)
            elif symbol == block:
                new_row.extend([*stones, *emptys, block])
                stones = []
                emptys = []

        new_row.extend([*stones, *emptys])
        new_record.append("".join(new_row))
    return new_record


def count_stones_weight(record: Record) -> int:
    return sum([row.count("O") * w for w, row in enumerate(record[::-1], 1)])


if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle: Puzzle = read_puzzle("small_input.txt")
        result = solve_puzzle(puzzle)
        print(result)
        assert 136 == result
    else:
        puzzle = read_puzzle("input.txt")
        print(solve_puzzle(puzzle))
