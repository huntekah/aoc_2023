from collections import defaultdict
from functools import cache, partial
from typing import Optional

import numpy as np
from tqdm import tqdm


def solve_puzzle(puzzle) -> int:
    rules = puzzle.split("\n\n")[0].splitlines()
    messages = puzzle.split("\n\n")[1].splitlines()
    rules_dict = {}  # {name: [(condition_name, condition_function)]}
    for rule in rules:
        name, conditions_raw = rule.split("{")
        conditions = conditions_raw.strip("}").split(",")
        conditions = [c.strip() for c in conditions]
        conditions_parsed = []
        for c in conditions:
            if ">" in c:
                n, vd = c.split(">")
                v, d = vd.split(":")
                # n is name, v is value, d is destination_name
                # conditions_parsed.append((n, lambda x: x > int(v), d))
                # rewrite above with partial
                conditions_parsed.append((n, partial(lambda x, v: x > v, v=int(v)), d))
            elif "<" in c:
                n, vd = c.split("<")
                v, d = vd.split(":")
                # conditions_parsed.append((n, lambda x: x < int(v), d))
                conditions_parsed.append((n, partial(lambda x, v: x > v, v=int(v)), d))
            else:
                conditions_parsed.append((None, lambda x: True, c))
            pass
        rules_dict[name] = conditions_parsed

    # for k, v in rules_dict.items():
    #     print(k, end="\t")
    #     for i, c in enumerate(v):
    #         print(f"{c[0]} -> {c[2]}", end="\t")
    #     print()
    s = 0
    for m in messages:
        values_raw = m.strip("{}").split(",")
        values = {n: int(v) for n, v in [v.split("=") for v in values_raw]}
        values[None] = 0  # handle last rule with no name
        name = "in"
        print(f"{name} ", end="")
        while True:
            conditions = rules_dict.get(name, [])
            for n, c, d in conditions:
                if n in values and c(values[n]):
                    print(f" -> {d}", end=" ")
                    name = d
                    break
            if name == "A":
                s += sum(values.values())
                print()
                break
            elif name == "R":
                print()
                break
            # print(".", end=" ")
    return s


def read_puzzle(input_file: str = "input.txt") -> str:
    with open(input_file, "r") as f:
        return f.read()


if __name__ == "__main__":
    SMALL = True
    if SMALL:
        puzzle = read_puzzle("small_input.txt")
        result = solve_puzzle(puzzle)
        print(result)
        assert 19114 == result
        assert 952408144115 == result
    else:
        puzzle = read_puzzle("input.txt")
        solution = solve_puzzle(puzzle)
        print(solution)
        assert solution < 643892
