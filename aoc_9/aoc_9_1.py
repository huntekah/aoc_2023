import inspect
from collections import Counter
from functools import cmp_to_key
from typing import Dict, Set, Tuple

from util.process_input import read_puzzle, Puzzle, string_of_numbers_to_list

Sequence = list[int]
Sequences = list[Sequence]
def solve_puzzle(puzzle: Puzzle) -> int:
    sequences = read_sequences(puzzle)
    values = [extrapolate_next_value(sequence) for sequence in sequences]
    return sum(values)

def read_sequences(puzzle: Puzzle) -> Sequences:
    return [string_of_numbers_to_list(line) for line in puzzle]

def extrapolate_next_value(sequence: Sequence) -> int:
    print(f"{inspect.stack()[0][3]}({sequence})")
    sequences: Sequences = [sequence]
    # We finish when sequence converges to all numbers being the same.
    while len(set(sequence)) != 1:
        # We might start with something like 10 13 16 21 30 45
        # Then we find difference between each consequent pair of numbers:
        # like:
        # 10  13  16  21  30  45
        #    3   3   5   9  15
        #      0   2   4   6
        #        2   2   2  <- here we can finish
        #          0   0

        sequence = extrapolate_next_sequence(sequence)
        sequences.append(sequence)

    # Add same number as last one in sequences[-1], then traverse sequence backwards
    # and append ( sequence[-1][-1] + sequence[-2][-1] ) to sequence[-2]
    # until we reach the beginning of sequences.
    # Then we return the last number in the first sequence.

    print(sequences)
    for i in range(len(sequences) - 2, -1, -1):
        # sequences[i].append(sequences[i][-1])
        # if i == len(sequences) - 1:
        #     continue
        # else:
        sequences[i].append(sequences[i][-1] + sequences[i + 1][-1])
    print("___")
    print(sequences)
    print(sequences[0][-1])
    return sequences[0][-1]
def extrapolate_next_sequence(sequence: Sequence) -> Sequence:
    """find difference between each consequent pair of numbers"""
    return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]

if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle: list[str] = read_puzzle("small_input.txt")
        assert 114 == solve_puzzle(puzzle)
        print(solve_puzzle(puzzle))
    else:
        puzzle = read_puzzle("input.txt")
        print(solve_puzzle(puzzle))
