import re


def read_puzzle():
    with open("input.txt", "r") as f:
    # with open("small_input_2.txt", "r") as f:
        return f.read().splitlines()


def solve_puzzle(puzzle):
    scratchcard_counts = {i: 1 for i in range(len(puzzle))}
    for i, line in enumerate(puzzle):
        scratchcard_copies = get_scratchcard_copies(line, i)
        print(f"Scratchcard {i}: {scratchcard_copies}")
        for copy, count in scratchcard_copies:
            scratchcard_counts[copy] += scratchcard_counts[i] * count
        print(f"Scratchcard counts: {scratchcard_counts}")

    return sum(scratchcard_counts.values())


def get_scratchcard_copies(line, i):
    winning_numbers = set(
        map(
            int, re.sub(" +", " ", line.split(":")[-1].split("|")[0]).strip().split(" ")
        )
    )
    my_numbers = set(
        map(
            int, re.sub(" +", " ", line.split(":")[-1].split("|")[1]).strip().split(" ")
        )
    )
    matches = len(winning_numbers.intersection(my_numbers))
    copies = [(j, 1) for j in range(i + 1, i + matches + 1)]
    return copies


if __name__ == "__main__":
    puzzle = read_puzzle()
    print(solve_puzzle(puzzle))
