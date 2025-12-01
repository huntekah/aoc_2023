from typing import Optional

from util.process_input import Puzzle, read_puzzle
import numpy as np
import z3

def solve(puzzle: Puzzle, start, end):
    hailstones = []
    score = 0
    for i, line in enumerate(puzzle):
        pos_raw, vel_raw = line.strip().split("@")
        pos = [int(p) for p in pos_raw.strip().split(",")]
        vel = [int(v) for v in vel_raw.strip().split(",")]
        hailstones.append((pos, vel))
    # for h1 in hailstones:
    #     for h2 in hailstones:
    #         for h3 in hailstones:
    #             if h1 == h2 or h1 == h3 or h2 == h3:
    #                 continue
    #             solve_with_matrix_inverse(h1,h2,h3)
    #             return
    print("_")
    h1,h2,h3 = hailstones[:3]
    solve_with_matrix_inverse(h1,h2,h3)
    print(len(hailstones))

def solve_with_matrix_inverse(h1,h2,h3):
    # We have 3 bullets travelling in 3D space. We know their position and velocity.
    # We want to find a 4-th bullet that will collide with all of them.
    # There fore bullet4 needs to be at the same place for each of the bullets, ath their collision time.
    # We can write this as a system of linear equations:
    # p1x + T1 * v1x = P4X + T1 * V4X
    # p1y + T1 * v1y = P4Y + T1 * V4Y
    # p1z + T1 * v1z = P4Z + T1 * V4Z
    
    # p2x + T2 * v2x = P4X + T2 * V4X
    # p2y + T2 * v2y = P4Y + T2 * V4Y
    # p2z + T2 * v2z = P4Z + T2 * V4Z
    
    # p1x - p2x + T1 * v1x - T2 * v2x = T1 * V4X - T2 * V4X
    # T1 * v1x - T2 * v2x - T1 * V4X - T2 * V4X = p2x - p1x
    # T1 (v1x - V4X) - T2 (v2x + V4X) = p2x - p1x
    # - V4X ( T1 + T2 ) + T1 v1x - T2 v2x = p2x - p1x
    # - V4X ( T1 + T3 ) + T1 v1x - T3 v3x = p3x - p1x
    # - V4X ( T2 + T3 ) + T2 v2x - T3 v3x = p3x - p2x
    # This should solve  4 variables...
    # Lets try to solve it with matrix inverse
    # A * X = B
    # X = A ** -1 * B

    T1, T2, T3, V4X, V4Y, V4Z, P4X, P4Y, P4Z = z3.Ints('T1 T2 T3 V4X V4Y V4Z P4X P4Y P4Z')
    solver = z3.Solver()

    (p1x,p1y,p1z), (v1x, v1y, v1z) = h1[0], h1[1]
    (p2x,p2y,p2z), (v2x, v2y, v2z) = h2[0], h2[1]
    (p3x,p3y,p3z), (v3x, v3y, v3z) = h3[0], h3[1]

    equations = [
        p1x + T1 * v1x == P4X + T1 * V4X,
        p1y + T1 * v1y == P4Y + T1 * V4Y,
        p1z + T1 * v1z == P4Z + T1 * V4Z,
        p2x + T2 * v2x == P4X + T2 * V4X,
        p2y + T2 * v2y == P4Y + T2 * V4Y,
        p2z + T2 * v2z == P4Z + T2 * V4Z,
        p3x + T3 * v3x == P4X + T3 * V4X,
        p3y + T3 * v3y == P4Y + T3 * V4Y,
        p3z + T3 * v3z == P4Z + T3 * V4Z,
    ]

    solver.add(*equations)
    solver.add(T1 >= 0)
    solver.add(T2 >= 0)
    solver.add(T3 >= 0)
    print(solver.check())
    print("___")
    s = solver.model()
    print(s)
    print(s[P4X] + s[P4Y] + s[P4Z])
    # print(solver.model())
    print("This is the test of ")
    #
    # A = np.array([
    #     # what we solve for
    #     # 1. col = -V4X ( T1 + T2 )
    #     # 2. col = -V4X ( T1 + T3 )
    #     # 3. col = -V4X ( T2 + T3 )
    #     # 4. col = T1
    #     # 5. col = T2
    #     # 6. col = T3
    #     [1,0,0,v1x,-v2x,0], # - V4X ( T1 + T2 ) + T1 v1x - T2 v2x = p2x - p1x
    #     [0,1,0,v1x,0,-v3x], # - V4X ( T1 + T3 ) + T1 v1x - T3 v3x = p3x - p1x
    #     [0,0,1,0,v2x,-v3x], # - V4X ( T2 + T3 ) + T2 v2x - T3 v3x = p3x - p2x
    #     [1,0,0,v1y,-v2y,0], # - V4Y ( T1 + T2 ) + T1 v1y - T2 v2y = p2x - p1x
    #     [0,1,0,v1y,0,-v3y], # - V4Y ( T1 + T3 ) + T1 v1y - T3 v3y = p3x - p1x
    #     [0,0,1,0,v2y,-v3y], # - V4Y ( T2 + T3 ) + T2 v2y - T3 v3y = p3x - p2x
    #     [1,0,0,v1z,-v2z,0], # - V4Z ( T1 + T2 ) + T1 v1z - T2 v2z = p2x - p1x
    #     [0,1,0,v1z,0,-v3z], # - V4Z ( T1 + T3 ) + T1 v1z - T3 v3z = p3x - p1x
    #     [0,0,1,0,v2z,-v3z], # - V4Z ( T2 + T3 ) + T2 v2z - T3 v3z = p3x - p2x
    # ])
    # B = np.array([
    #     [p2x - p1x],
    #     [p3x - p1x],
    #     [p3x - p2x],
    #     [p2y - p1y],
    #     [p3y - p1y],
    #     [p3y - p2y],
    #     [p2z - p1z],
    #     [p3z - p1z],
    #     [p3z - p2z],
    # ])
    # print()
    #
    # # p + t_1 * v = p_1 + t_1 * v_1
    # # t_1 * v + p - v_1 * t_1 = p_1
    # # t1 * vx + px - v1x * t1 = p1x
    # # lets assume that t2 = 0 for v2
    # # 0       + px - 0        = p1x
    # # [1,0,0,1,0,0,-v1x,0,0] **-1 * [t1 * vx, px, t1] = [p1x]
    # # A = np.array([
    # #     #t1 * vx, px, t1
    # #     [1,1,-v1x],
    # #     [0,1,0],
    # #     [1,1,-v3x]
    # # ])
    # # B = np.array([
    # #     [p1x],
    # #     [p2x],
    # #     [p3x]
    # # ])
    # #######
    # # A = np.array([
    # #         #t1 * vx, px, t1
    # #         #t1 * vy, py, t1
    # #         #t1 * vz, pz, t1
    # #         [1,0,0,1,0,0,-v1x,0   ,   0],
    # #         [0,1,0,0,1,0,   0,-v1y,   0],
    # #         [0,0,1,0,0,1,   0,   0,-v1z],
    # #         [0,0,0,1,0,0,   0,   0,   0],
    # #         [0,0,0,0,1,0,   0,   0,   0],
    # #         [0,0,0,0,0,1,   0,   0,   0],
    # #         [1,0,0,1,0,0,-v3x,   0,   0],
    # #         [0,1,0,0,1,0,   0,-v3y,   0],
    # #         [0,0,1,0,0,1,   0,   0,-v3z],
    # #     ])
    # # B =  np.array([
    # #         [p1x],
    # #         [p1y],
    # #         [p1z],
    # #         [p2x],
    # #         [p2y],
    # #         [p2z],
    # #         [p3x],
    # #         [p3y],
    # #         [p3z],
    # #     ])
    #
    #
    # # print(A)
    # try:
    #     X = np.linalg.solve(A,B)
    #     print(X)
    #     print()
    #
    # except np.linalg.LinAlgError:
    #     # print('e')
    #     pass

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
