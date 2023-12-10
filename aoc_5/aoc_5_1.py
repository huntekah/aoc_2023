import re
def read_puzzle():
    with open("input.txt", "r") as f:
    # with open("small_input.txt", "r") as f:
        return f.read().splitlines()

def solve_puzzle(puzzle):
    result = 0
    seeds = get_seeds(puzzle)
    mappings = get_mappings(puzzle)
    print(mappings)
    final_seeds = transform_seeds(seeds, mappings)
    return min(final_seeds)

def get_seeds(puzzle):
    seeds = string_of_numbers_to_list(puzzle[0].split(":")[-1])
    return seeds

def get_mappings(puzzle):
    mappings = {}
    n = -1
    for line in puzzle[1:]:
        if ":" in line:
            n += 1
            mappings[n] = []
            continue
        elif line.strip() == "":
            pass
        else:
            d,s,r = string_of_numbers_to_list(line)
            mappings[n].append((d,s,r))
    return mappings


def transform_seeds(seeds, mappings):
    final_seeds = []
    for seed in seeds:
        for mapping in mappings.values():
            for d,s,r in mapping:
                if seed >= s and seed < s + r:
                    seed = seed + d - s
                    break
        final_seeds.append(seed)
    return final_seeds

def string_of_numbers_to_list(line):
    return map(int, re.sub(" +", " ", line).strip().split(" "))



if __name__ == "__main__":
    puzzle = read_puzzle()
    print(solve_puzzle(puzzle))