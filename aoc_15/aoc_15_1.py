import inspect
import re
from functools import cache
from itertools import product

from tqdm import tqdm


def solve_puzzle(puzzle) -> int:
    return sum([hash_step(step) for step in puzzle])


def hash_step(s: str) -> int:
    """Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256."""
    v = 0
    for c in s:
        v = (v + ord(c)) * 17 % 256
    return v


def read_puzzle(filename: str):
    return [a.strip() for a in open(filename).read().split(",")]


if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle = read_puzzle("small_input.txt")
        result = solve_puzzle(puzzle)
        print(result)
        assert 1320 == result
    else:
        puzzle = read_puzzle("input.txt")
        print(solve_puzzle(puzzle))
