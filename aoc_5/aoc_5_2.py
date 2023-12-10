import re
def read_puzzle():
    with open("input.txt", "r") as f:
    # with open("small_input.txt", "r") as f:
        return f.read().splitlines()

def solve_puzzle(puzzle):
    result = 0
    seed_ranges = get_seed_ranges(puzzle)
    seeds = get_seeds(seed_ranges)
    mappings = get_mappings(puzzle)
    print(mappings)
    final_seeds = transform_seeds(seeds, mappings)
    return min(final_seeds)

def get_seed_ranges(puzzle):
    numbers = string_of_numbers_to_list(puzzle[0].split(":")[-1])
    print(numbers)
    ranges = [(a,b) for a,b in zip(numbers[::2], numbers[1::2])]
    print(ranges)
    return ranges

def get_seeds(seed_ranges):
    seeds = [n for a,b in seed_ranges for n in range(a,a+b)]
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
    return list(map(int, re.sub(" +", " ", line).strip().split(" ")))



if __name__ == "__main__":
    puzzle = read_puzzle()
    print(solve_puzzle(puzzle))