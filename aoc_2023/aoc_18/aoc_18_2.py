from collections import defaultdict
from functools import cache
from typing import Optional

import numpy as np
from tqdm import tqdm

from util.process_input import Puzzle, read_puzzle


def solve_puzzle(puzzle: Puzzle) -> int:
    boundaries = [(0, 0)]
    x, y = 0, 0
    bnd_len = 0
    for line in puzzle:
        i, d, h = line.split()
        # d = int(d)
        # i = {"R": 0, "D": 1, "L": 2, "U": 3}[i]
        h = h.strip("()")
        d, i = int(float.fromhex(h[1:-1])), int(h[-1])
        # print(d,i)
        # i like 0=R for right, 2=L for left, 3=U for up, 1=D for down
        # d-=1
        if i == 0:
            boundaries.append((y, x + d))
            x += d
        elif i == 2:
            boundaries.append((y, x - d))
            x -= d
        elif i == 3:
            boundaries.append((y - d, x))
            y -= d
        elif i == 1:
            boundaries.append((y + d, x))
            y += d
        else:
            raise Exception("Unknown direction")
        bnd_len += d
        # print(bnd_len)
    # shoelace formula
    # https://en.wikipedia.org/wiki/Shoelace_formula
    # https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
    x = np.array([x for x, y in boundaries])
    y = np.array([y for x, y in boundaries])
    return (
        int(0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1))))
        + bnd_len / 2
        + 1
    )

    # find middle of boundaries
    # xm = (min([x for x,y in boundaries]) + max([x for x,y in boundaries])) //  2
    # ym = (min([y for x,y in boundaries]) + max([y for x,y in boundaries])) // 2

    # pixels_in_boundaries = flood_fill(boundaries,(-5,-1))
    # print(xm,ym)
    # print(boundaries)
    # pixels_in_boundaries = span_flood_fill(boundaries,(1,1))
    # pixels_in_boundaries = flood_fill(boundaries,(xm,ym))

    # return bnd_len #+ pixels_in_boundaries


if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle = read_puzzle("small_input.txt")
        result = solve_puzzle(puzzle)
        print(result)
        assert 62 == result
        assert 952408144115 == result
    else:
        puzzle = read_puzzle("input.txt")
        solution = solve_puzzle(puzzle)
        print(solution)
        # assert  solution
