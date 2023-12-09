import re
def read_puzzle():
    with open("input.txt", "r") as f:
    # with open("small_input.txt", "r") as f:
        return f.read().splitlines()


def solve_puzzle(puzzle):
    result = 0
    for line in puzzle:
        score = get_score(line)
        result += score
    return result


def get_score(line):
    # print(line.split(":")[-1].split("|")[0].strip().split(" "))
    # print(line.split(":")[-1].split("|")[1].strip().split(" "))
    winning_numbers = set(
        map(int, re.sub(" +"," ",line.split(":")[-1].split("|")[0]).strip().split(" "))
    )
    my_numbers = set(
        map(int, re.sub(" +"," ",line.split(":")[-1].split("|")[1]).strip().split(" "))
    )
    print(f"Winning numbers: {winning_numbers}")
    print(f"My numbers: {my_numbers}")
    matches =  len(winning_numbers.intersection(my_numbers))
    score = int(2 ** (matches-1))
    print(f"Matches: {matches}")
    print(f"Score: {score}")
    print(f"Intersection: {winning_numbers.intersection(my_numbers)}")
    print()
    return score


if __name__ == "__main__":
    puzzle = read_puzzle()
    print(solve_puzzle(puzzle))
