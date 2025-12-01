from collections import defaultdict
from functools import cache
from typing import Optional

from tqdm import tqdm

from util.process_input import Puzzle, read_puzzle


def solve_puzzle(puzzle: Puzzle) -> int:
    boundaries = [(0, 0)]
    x, y = 0, 0
    bnd_len = 0
    for line in puzzle:
        i, d, h = line.split()
        # i like R for right, L for left, U for up, D for down
        d = int(d)
        if i == "R":
            boundaries.extend([(y, i) for i in range(x + 1, x + d + 1)])
            x += d
        elif i == "L":
            boundaries.extend([(y, i) for i in range(x - 1, x - d - 1, -1)])
            x -= d
        elif i == "U":
            boundaries.extend([(i, x) for i in range(y - 1, y - d - 1, -1)])
            y -= d
        elif i == "D":
            boundaries.extend([(i, x) for i in range(y + 1, y + d + 1)])
            y += d
        else:
            raise Exception("Unknown direction")
        bnd_len += d
        # print(bnd_len)

    # find middle of boundaries
    xm = (min([x for x, y in boundaries]) + max([x for x, y in boundaries])) // 2
    ym = (min([y for x, y in boundaries]) + max([y for x, y in boundaries])) // 2

    # pixels_in_boundaries = flood_fill(boundaries,(-5,-1))
    print(xm, ym)
    print(boundaries)
    pixels_in_boundaries = flood_fill(boundaries, (1, 1))
    # pixels_in_boundaries = flood_fill(boundaries,(xm,ym))

    return bnd_len + pixels_in_boundaries


def flood_fill(boundaries, start):
    pixels_in_boundaries = 0
    active_pixels = {start}
    used_pixels = []
    t = tqdm(total=1)
    while len(active_pixels) > 0:
        t.total = len(active_pixels)
        t.update()
        t.refresh()
        c_pixel = active_pixels.pop()
        # print(c_pixel)
        if c_pixel in used_pixels:
            continue
        used_pixels.append(c_pixel)
        if c_pixel in boundaries:
            # print("boundary")
            continue
        pixels_in_boundaries += 1
        neighbours = get_neighbours(c_pixel)
        for n in neighbours:
            if n not in used_pixels:
                active_pixels.add(n)
    return pixels_in_boundaries


def get_neighbours(pixel):
    x, y = pixel
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]


if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle = read_puzzle("small_input.txt")
        result = solve_puzzle(puzzle)
        print(result)
        assert 62 == result
    else:
        puzzle = read_puzzle("input.txt")
        solution = solve_puzzle(puzzle)
        print(solution)
        # assert  solution
