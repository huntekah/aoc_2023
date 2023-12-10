import re
def read_puzzle(input_file="input.txt"):
    with open(input_file, "r") as f:
        return f.read().splitlines()


def string_of_numbers_to_list(line):
    return list(map(int, re.sub(" +", " ", line).strip().split(" ")))

