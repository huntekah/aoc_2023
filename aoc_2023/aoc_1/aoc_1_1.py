import re


def read_puzzle():
    with open("input.txt", "r") as f:
        # with open("small_input.txt", "r") as f:
        return f.read().splitlines()


def replace_text_to_numbers(puzzle):
    # one, two, three, four, five, six, seven, eight, and nine
    numbers_map = {
        "eightwo": "82",
        "oneight": "18",
        "twone": "21",
        "threeight": "38",
        "fiveight": "58",
        "sevenine": "79",
        "eighthree": "83",
        "nineight": "98",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    # puzzle2 = list(
    #     map(
    #         lambda line: re.compile("|".join(numbers_map.keys())).sub(
    #             lambda m: str(numbers_map[re.escape(m.group(0))]), line
    #         ),
    #         puzzle,
    #     )
    # )
    puzzle2 = []
    for line in puzzle:
        for key, value in numbers_map.items():
            line = line.replace(key, value)
        puzzle2.append(line)
    print("\n".join([str({a: b}) for a, b in zip(puzzle, puzzle2)]))
    # print(list(puzzle2))
    return puzzle2


def solve_puzzle(puzzle):
    sum_of_coordinates = 0
    puzzle_with_numbers = replace_text_to_numbers(puzzle)
    # print("\n".join(list(puzzle)))
    for old_line, line in zip(puzzle, puzzle_with_numbers):
        # find first and last digit in line
        numbers = re.sub(r"[^0-9]", "", line)
        coordinates = 10 * int(numbers[0]) + int(numbers[-1])
        sum_of_coordinates += coordinates
        print(f"{old_line}\n{line}\n{numbers} -> {coordinates}\n______")
    return sum_of_coordinates


if __name__ == "__main__":
    puzzle = read_puzzle()
    print(solve_puzzle(puzzle))
