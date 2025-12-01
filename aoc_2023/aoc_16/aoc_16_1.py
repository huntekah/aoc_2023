import inspect
import re
from collections import defaultdict
from functools import cache
from itertools import product
from typing import Optional

from tqdm import tqdm

from util.process_input import read_puzzle

Location = tuple[int, int]
# binary 0 or 1 for each direction: up, right, down, left
UP = 0b0001  # 1
RIGHT = 0b0010  # 2
DOWN = 0b0100  # 4
LEFT = 0b1000  # 8
Directions = int
Field = tuple[str]
Rays = dict[Location, Directions]  # I can extract active rays from this
# ActiveRays = list[tuple[Location, Directions]]


def solve_puzzle(puzzle) -> int:
    field = Field(puzzle)
    active_rays: Rays = defaultdict(lambda: 0)
    active_rays[(0, -1)] |= RIGHT
    used_rays: Rays = defaultdict(lambda: 0)

    t = tqdm(total=1)
    while len(active_rays) > 0:
        l, d = next(iter(active_rays.items()))
        for d1 in range(4):
            d1 = 1 << d1
            if d & d1:
                move(l, d1, active_rays, used_rays, field)
                # used_rays[(l, d1)] = True
            t.update()
            t.refresh()
            t.total = sum([bin(v).count("1") for v in active_rays.values()])
        # show_rays(active_rays)
        # show_used_rays(used_rays, field)
    show_energy_field(used_rays, field)
    return count_score(used_rays, field)


def count_score(used_rays: Rays, field: Field) -> int:
    """Count number of fields with at least one ray in them"""
    return sum(
        [
            1
            for r, row in enumerate(field)
            for c, _ in enumerate(row)
            if used_rays.get((r, c))
        ]
    )


def move(
    location: Location,
    direction: Directions,
    active_rays: Rays,
    used_rays: Rays,
    field: Field,
) -> None:
    """Move ray to next field

    1. Add ray to used rays
    2. Remove ray from active rays
    3. Add new rays to active rays if they are not in used rays
    """
    # add ray to used rays
    used_rays[location] |= direction

    # remove direction from active rays like 0b1101 - 0b0100 = 0b1001
    active_rays[location] = (
        active_rays[location] & ~direction
    )  # works, cause we are sure that direction is in active_rays
    if active_rays[location] == 0:
        del active_rays[location]

    # add new rays to active rays
    direction_to_location = {
        UP: lambda y, x: (y - 1, x),  # up
        RIGHT: lambda y, x: (y, x + 1),  # right
        DOWN: lambda y, x: (y + 1, x),  # down
        LEFT: lambda y, x: (y, x - 1),  # left
    }
    x, y = direction_to_location[direction](*location)

    ## check if ray is out of bounds
    if x < 0 or x >= len(field) or y < 0 or y >= len(field[0]):
        return

    symbol = field[x][y]

    # add new rays if encountered a mirror like / or \, just move if encountered a .
    if symbol == ".":
        # ray is out of bounds
        active_rays[(x, y)] |= direction
    elif symbol == "/":
        # ray is reflected
        # up + / = right # 0b0001 << 1 = 0b0010
        # right + / = up # 0b0010 >> 1 = 0b0001
        # down + / = left # 0b0100 << 1 = 0b1000
        # left + / = down # 0b1000 >> 1 = 0b0100
        if direction == UP:  # up -> right
            update_ray_if_not_used(active_rays, used_rays, (x, y), RIGHT)
            # active_rays[(x, y)] |= RIGHT
        elif direction == RIGHT:  # right -> up
            update_ray_if_not_used(active_rays, used_rays, (x, y), UP)
            # active_rays[(x, y)] |= UP
        elif direction == DOWN:  # down -> left
            update_ray_if_not_used(active_rays, used_rays, (x, y), LEFT)
            # active_rays[(x, y)] |= LEFT
        elif direction == LEFT:  # left -> down
            update_ray_if_not_used(active_rays, used_rays, (x, y), DOWN)
            # active_rays[(x, y)] |= DOWN
    elif symbol == "\\":
        # up + \ = left # 0b0001 >> 1 = 0b1000
        # right + \ = down # 0b0010 << 1 = 0b0100
        # down + \ = right # 0b0100 >> 1 = 0b0010
        # left + \ = up # 0b1000 << 1 = 0b0001
        if direction == UP:
            # active_rays[(x, y)] |= LEFT
            update_ray_if_not_used(active_rays, used_rays, (x, y), LEFT)
        elif direction == RIGHT:
            # active_rays[(x, y)] |= DOWN
            update_ray_if_not_used(active_rays, used_rays, (x, y), DOWN)
        elif direction == DOWN:
            # active_rays[(x, y)] |= RIGHT
            update_ray_if_not_used(active_rays, used_rays, (x, y), RIGHT)
        elif direction == LEFT:
            # active_rays[(x, y)] |= UP
            update_ray_if_not_used(active_rays, used_rays, (x, y), UP)
    elif symbol == "|":
        # up + | = up
        # right + | = UP + DOWN
        # down + | = down
        # left + | = UP + DOWN
        if direction == RIGHT or direction == LEFT:
            # active_rays[(x, y)] |= UP | DOWN
            update_ray_if_not_used(active_rays, used_rays, (x, y), UP)
            update_ray_if_not_used(active_rays, used_rays, (x, y), DOWN)
        else:
            # active_rays[(x, y)] |= direction
            update_ray_if_not_used(active_rays, used_rays, (x, y), direction)
    elif symbol == "-":
        # up + - = LEFT + RIGHT
        # right + - = right
        # down + - = LEFT + RIGHT
        # left + - = left
        if direction == UP or direction == DOWN:
            # active_rays[(x, y)] |= LEFT | RIGHT
            update_ray_if_not_used(active_rays, used_rays, (x, y), LEFT)
            update_ray_if_not_used(active_rays, used_rays, (x, y), RIGHT)
        else:
            # active_rays[(x, y)] |= direction
            update_ray_if_not_used(active_rays, used_rays, (x, y), direction)


def update_ray_if_not_used(
    active_rays: Rays, used_rays: Rays, location: Location, direction: Directions
) -> None:
    """Update ray if it is not used"""
    if not used_rays[location] & direction:
        active_rays[location] |= direction


def show_rays(active_rays: Rays) -> None:
    """Show rays in a field"""
    # find min and max x and y
    min_x = min([l[0] for l in active_rays.keys()])
    max_x = max([l[0] for l in active_rays.keys()])
    min_y = min([l[1] for l in active_rays.keys()])
    max_y = max([l[1] for l in active_rays.keys()])

    # create a field
    field = [[" " for _ in range(max_y - min_y + 1)] for _ in range(max_x - min_x + 1)]

    # fill field with rays
    for l, d in active_rays.items():
        x = l[0] - min_x
        y = l[1] - min_y
        field[x][y] = str(d)

    # print field
    print("Field:")
    for row in field:
        print("".join(row))
    print()


def show_used_rays(used_rays: Rays, field: Field) -> None:
    """Show used rays in a field"""
    for i, row in enumerate(field):
        for j, symbol in enumerate(row):
            if symbol == ".":
                if ray := used_rays.get((i, j)):
                    print(ray, end="")
                else:
                    print(".", end="")
            else:
                print(symbol, end="")
        print()
    print()


def show_energy_field(used_rays: Rays, field: Field) -> None:
    """Show energy field"""
    for i, row in enumerate(field):
        for j, symbol in enumerate(row):
            if used_rays.get((i, j)):
                print("#", end="")
            else:
                print(".", end="")
        print()
    print()


if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle = read_puzzle("small_input3.txt")
        result = solve_puzzle(puzzle)
        print(result)
        assert 46 == result
    else:
        puzzle = read_puzzle("input.txt")
        solution = solve_puzzle(puzzle)
        # assert X == solution
        print(solution)
