import inspect
import re
from collections import defaultdict
from functools import cache
from itertools import product

from tqdm import tqdm

from util.process_input import Puzzle, read_puzzle, string_of_numbers_to_list

Record = list[str]
URecord = tuple[str]


def solve_puzzle(puzzle: URecord) -> int:
    record: URecord = puzzle
    score = count_stones_weight(record)
    # print(count_stones_weight(slide_stones_up(record)))

    print("\n".join(record), end="\n\n")
    repetitions = 1000000000
    visited_records = defaultdict(list)
    visited_records[record].append((0, score))
    loop_end = None
    for n in range(repetitions):
        record = full_spin_backwards(record)
        score = count_stones_weight(record)
        h = hash("".join(record)) // 10**16
        print(f"{n+1:<4} Weight: {score:<4} Hash: {h:>4}")
        if record in visited_records.keys():
            # visited_records[record].append((n + 1, score))
            loop_end = n
            print("Found loop!")
            break
        visited_records[record].append((n + 1, score))
    loop_start = visited_records[record][0][0]
    # loop_end = len(repetitions)
    loop_length = loop_end - loop_start + 1
    print(f"{loop_start=}, {loop_end=}, {loop_length=}")
    print(f"{repetitions % loop_length=}")
    final_score = [
        a[0][1]
        for a in visited_records.values()
        if (a[0][0] % loop_length == repetitions % loop_length) and (a[0][0] > loop_start)
    ][0]
    return final_score


def rotate_90_clockwise(record: URecord) -> URecord:
    return rotate_90_counter_clockwise(
        rotate_90_counter_clockwise(rotate_90_counter_clockwise(record))
    )


@cache
def rotate_90_counter_clockwise(record: URecord) -> URecord:
    return tuple("".join(x[::-1]) for x in list(zip(*record)))


def rotate_180(record: URecord) -> URecord:
    return rotate_90_counter_clockwise(rotate_90_counter_clockwise(record))


@cache
def slide_stones_left(record: URecord) -> URecord:
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
    return unmutable_record(new_record)


def slide_stones_up(record: URecord) -> URecord:
    return rotate_90_clockwise(slide_stones_right(rotate_90_counter_clockwise(record)))


def slide_stones_right(record: URecord) -> URecord:
    return rotate_180(slide_stones_left(rotate_180(record)))


def slide_stones_down(record: URecord) -> URecord:
    return rotate_90_clockwise(slide_stones_left(rotate_90_counter_clockwise(record)))


def count_stones_weight(record: URecord) -> int:
    return sum([row.count("O") * w for w, row in enumerate(record[::-1], 1)])


@cache
def full_spin(record: URecord) -> URecord:
    modifications = [
        slide_stones_up,
        slide_stones_right,
        slide_stones_down,
        slide_stones_left,
    ]
    for slide in modifications:
        record = slide(record)
        print("_")
        print("\n".join(record))
    # record = slide_stones_up(slide_stones_right(slide_stones_down(slide_stones_left(record))))
    return record


@cache
def full_spin_backwards(record: URecord) -> URecord:

    modifications = [
        (slide_stones_up, "up"),
        (slide_stones_left, "left"),
        (slide_stones_down, "down"),
        (slide_stones_right, "right"),
    ]
    for slide, name in modifications:
        record = slide(record)
        # print(f"_{name} spin_")
        # print("\n".join(record), end="\n\n")
    # record = slide_stones_up(slide_stones_left(slide_stones_down(slide_stones_right(record))))
    return record


def unmutable_record(record: Record) -> URecord:
    return tuple(record)


if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle: URecord = unmutable_record(read_puzzle("small_input.txt"))
        result = solve_puzzle(puzzle)
        print(result)
        assert 64 == result
    else:
        puzzle = unmutable_record(read_puzzle("input.txt"))
        print(solve_puzzle(puzzle))

# not 101568
