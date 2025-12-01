from functools import reduce


def read_puzzle():
    with open("input.txt", "r") as f:
        # with open("small_input.txt", "r") as f:
        return f.read().splitlines()


def solve_puzzle(puzzle):
    result = 0
    for i, line in enumerate(puzzle):
        max_of_colors = get_highest_color_counts(line)
        result += reduce((lambda x, y: x * y), max_of_colors)
    return result


def get_highest_color_counts(line):
    max_r = 0
    max_g = 0
    max_b = 0
    for part in line.split(":")[-1].split(";"):
        r, g, b = get_part_color_counts(part)
        max_r = max(max_r, r)
        max_g = max(max_g, g)
        max_b = max(max_b, b)
    return max_r, max_g, max_b


def get_part_color_counts(part):
    cubes = part.split(",")
    r, g, b = 0, 0, 0
    for cube in cubes:
        count, color = cube.strip().split(" ")
        if color == "red":
            r = int(count)
        elif color == "green":
            g = int(count)
        elif color == "blue":
            b = int(count)
    return r, g, b


if __name__ == "__main__":
    puzzle = read_puzzle()
    print(solve_puzzle(puzzle))
