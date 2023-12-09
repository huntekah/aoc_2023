def read_puzzle():
    with open("input.txt", "r") as f:
        # with open("small_input.txt", "r") as f:
        return f.read().splitlines()


def solve_puzzle(puzzle):
    cube_counts = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    result = 0
    for i, line in enumerate(puzzle):
        if is_possible(line, cube_counts):
            print(f"Game {i + 1} is possible")
            result += i + 1
    return result


def is_possible(line, cube_counts):
    for part in line.split(":")[-1].split(";"):
        if not is_part_possible(part, cube_counts):
            return False
    return True


def is_part_possible(part, cube_counts):
    cubes = part.split(",")
    for cube in cubes:
        # print(cube)
        count, color = cube.strip().split(" ")
        if int(count) > cube_counts[color]:
            return False
    return True


if __name__ == "__main__":
    puzzle = read_puzzle()
    print(solve_puzzle(puzzle))
