"""If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361."""


def read_puzzle():
    with open("input.txt", "r") as f:
        # with open("small_input.txt", "r") as f:
        return f.read().splitlines()


def solve_puzzle(puzzle):
    result = 0
    for i, line in enumerate(puzzle):
        result += get_sum_of_adjacent_numbers(line, puzzle, i)
    return result


def get_sum_of_adjacent_numbers(line, puzzle, i):
    result = 0
    number = 0
    is_adjacent = False
    for j, char in enumerate(line):
        if char.isdigit():
            number = number * 10 + int(char)
            if not is_adjacent:
                is_adjacent = check_if_adjacent(puzzle, i, j)
        else:
            if is_adjacent:
                print(f"OK {number}")
                result += number
            elif number != 0:
                print(f"BAD {number}")
            number = 0
            is_adjacent = False
    else:
        if is_adjacent:
            print(f"OK {number}")
            result += number
    return result


def check_if_adjacent(puzzle, i, j):
    fields_to_check = [
        (i - 1, j - 1),
        (i - 1, j),
        (i - 1, j + 1),
        (i, j - 1),
        (i, j + 1),
        (i + 1, j - 1),
        (i + 1, j),
        (i + 1, j + 1),
    ]
    for field in fields_to_check:
        if (
            field[0] >= 0
            and field[1] >= 0
            and field[0] < len(puzzle)
            and field[1] < len(puzzle[0])
        ):
            if check_field(field, puzzle):
                return True


def check_field(field, puzzle):
    i, j = field
    check = (not puzzle[i][j].isdigit()) and (puzzle[i][j] != ".")
    print(f"Checking {i} {j} -> {puzzle[i][j]} is {check}")
    return check


if __name__ == "__main__":
    puzzle = read_puzzle()
    print(solve_puzzle(puzzle))
