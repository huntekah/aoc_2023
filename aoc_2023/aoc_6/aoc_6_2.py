import re
from math import ceil, floor, sqrt

from util.process_input import read_puzzle, string_of_numbers_to_list


def solve_puzzle(puzzle):
    result = 1
    times = string_of_numbers_to_list(re.sub(" ", "", puzzle[0].split(":")[-1]))
    distances = string_of_numbers_to_list(re.sub(" ", "", puzzle[1].split(":")[-1]))

    for time, distance in zip(times, distances):
        x = count_ways_to_beat_record(time, distance)
        result *= x
    print(f"{times=}\n{distances=}")
    return result


### EQUATION
"""xt -> acceleration button duration
y  -> distance travelled
T  -> race_duration
v  -> boat velocity
D  -> race best distance

xt = v


y = v * (T - xt)
D < y

D < v * (T - v)
D < Tv - v**2
0 < -v**2 + Tv - D
a = -1
b = T
c = -D

d = (b ** 2) - (4 * a * c)

# find two solutions
x1 = (-b - sqrt(d)) / (2 * a)
x2 = (-b + sqrt(d)) / (2 * a)

"""


def count_ways_to_beat_record(T, D):
    a = -1
    b = T
    c = -D
    x1, x2 = solve_quadratic_equation(a, b, c)
    print(x1, x2)
    if x1 == floor(x1):
        x1 += 1
    if x2 == ceil(x2):
        x2 -= 1
    solutions = len(range(ceil(x1), floor(x2))) + 1
    print((ceil(x1), floor(x2)), solutions)
    return solutions


def solve_quadratic_equation(a, b, c):
    d = (b**2) - (4 * a * c)

    # find two solutions
    x1 = (-b - sqrt(d)) / (2 * a)
    x2 = (-b + sqrt(d)) / (2 * a)
    return min(x1, x2), max(x1, x2)


if __name__ == "__main__":
    # puzzle = read_puzzle("small_input.txt")
    puzzle = read_puzzle()
    print(solve_puzzle(puzzle))
