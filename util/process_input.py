import re

Puzzle = list[str]
def read_puzzle(input_file: str = "input.txt") -> Puzzle:
    with open(input_file, "r") as f:
        return f.read().splitlines()


def string_of_numbers_to_list(line: str) -> list[int]:
    return list(map(int, re.sub(" +", " ", line).strip().split(" ")))
