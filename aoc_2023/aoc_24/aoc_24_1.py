from typing import Optional

from util.process_input import Puzzle, read_puzzle


def solve(puzzle: Puzzle, start, end):
    hailstones = []
    score = 0
    for i, line in enumerate(puzzle):
        pos_raw, vel_raw = line.strip().split("@")
        pos = [int(p) for p in pos_raw.strip().split(",")]
        vel = [int(v) for v in vel_raw.strip().split(",")]
        hailstones.append((pos, vel))
        for j, h2 in enumerate(hailstones):
            if i == j:
                continue
            if c := collision(hailstones[i], h2):
                h1_time = get_collision_time(*hailstones[i][0][:2], *hailstones[i][1][:2], *c)
                h2_time = get_collision_time(*h2[0][:2], *h2[1][:2], *c)
                is_valid = all([start <= c[0] <= end, start <= c[1] <= end, h1_time > 0, h2_time > 0])
                # print(i, j, c, is_valid)
                # h1_time = get_collision_time(*hailstones[i][0][:2], *hailstones[i][1][:2], *c)
                # h2_time = get_collision_time(*h2[0][:2], *h2[1][:2], *c)
                # print(f"\t\t{h1_time}\n\t\t{h2_time}")
                #
                if is_valid:
                    print(f"\t{pos} @ {vel}")
                    print(f"\t{h2[0]} @ {h2[1]}")
                score += is_valid

    return score


def collision(h1, h2) -> Optional[tuple[int, int]]:
    (x1, y1, _), (vx1, vy1, _) = h1
    (x2, y2, _), (vx2, vy2, _) = h2
    # How to compute the intersection of two lines
    # ax + b = cx + d
    # x(a-c) +b - d = 0
    # x = (d-b)/(a-c) if a != c | elif d == b -> the same | else None
    a, b = (vy1 / vx1, y1 - (vy1 / vx1) * x1) if vx1 != 0 else (None, x1)
    c, d = (vy2 / vx2, y2 - (vy2 / vx2) * x2) if vx2 != 0 else (None, x2)
    if a == c:
        return None
    elif a is None:
        return (b, c * b + d)
    elif c is None:
        return (d, a * d + b)
    else:
        return ((d - b) / (a - c), (a * d - b * c) / (a - c))


def get_collision_time(x1, y1, vx1, vy1, col_x, col_y):
    # We start at x1,y1 with velocity vx1, vy1. Knowing that we go throught col_x,col_y, find out whether it was in the future or in the past
    if vx1 == 0:
        return (col_x - x1) / vy1
    elif vy1 == 0:
        return (col_y - y1) / vx1
    else:
        return (
            (col_x - x1) / vx1
            if abs((col_x - x1) / vx1) < abs((col_y - y1) / vy1)
            else (col_y - y1) / vy1
        )


if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle = read_puzzle("small_input.txt")
        result = solve(puzzle, 7, 27)
        print(result)
        assert 2 == result
    else:
        puzzle = read_puzzle("input.txt")
        solution = solve(puzzle, 200000000000000, 400000000000000)
        print(solution)
