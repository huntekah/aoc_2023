import re


def read_puzzle():
    with open("input.txt", "r") as f:
        # with open("small_input.txt", "r") as f:
        return f.read().splitlines()


def solve_puzzle(puzzle):
    result = 0
    seed_ranges = get_seed_ranges(puzzle)
    # seeds = get_seeds(seed_ranges)
    mappings = get_mappings(puzzle)
    # print("MAPPINGS")
    # print(mappings)
    # print()
    final_seeds = transform_seed_ranges(seed_ranges, mappings)
    # print(sorted(final_seeds))
    return min(final_seeds)


def get_seed_ranges(puzzle):
    numbers = string_of_numbers_to_list(puzzle[0].split(":")[-1])
    # print(numbers)
    ranges = [(a, a + b - 1) for a, b in zip(numbers[::2], numbers[1::2])]
    # print(ranges)
    return ranges


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
            d, s, r = string_of_numbers_to_list(line)
            mappings[n].append((d, s, r))
    return mappings


def transform_seed_ranges(seed_ranges, mappings):
    # final_seeds = []
    ranges_after_mapping = []
    used_ranges = []
    for i, mapping in enumerate(mappings.values()):
        # print(f"MAP {i}")
        for d, s, r in mapping:
            for seed_range in seed_ranges:
                # print(f"\t{seed_range=}\t{s=}\t{s+r-1=}\t{d=}-{d+r-1}")
                if intersection := range_intersection(seed_range, (s, s + r - 1)):
                    # print(f"SR: {seed_range} S,S+R: {s, s+r} I: {intersection}")
                    ranges_after_mapping.append(
                        (intersection[0] + d - s, intersection[-1] + d - s)
                    )
                    used_ranges.append(intersection)
                    # print(f"mapping {seed_range} to {intersection[0] + d - s, intersection[-1] + d - s}")
        # print("___")
        unmapped_ranges = get_unmapped_ranges(set(seed_ranges), set(used_ranges))
        # print(f"Unmapped ranges: {unmapped_ranges}")
        # print(f"Ranges after mapping: {sorted(set(ranges_after_mapping))}")
        # print("______________________")
        seed_ranges = sorted(unmapped_ranges + ranges_after_mapping)
        used_ranges = []
        ranges_after_mapping = []

    # for seed in seeds:
    #     for mapping in mappings.values():
    #         for d, s, r in mapping:
    #             if seed >= s and seed < s + r:
    #                 seed = seed + d - s
    #                 break
    #     final_seeds.append(seed)
    return seed_ranges


def range_intersection(r1, r2):
    a, b = min(r1), max(r1)
    c, d = min(r2), max(r2)
    start = max(a, c)
    end = min(b, d)
    return (start, end) if start <= end else None


def range_union(r1, r2):
    a, b = min(r1), max(r1)
    c, d = min(r2), max(r2)
    start = min(a, c)
    end = max(b, d)
    return (start, end) if start <= end else None


def range_difference(r1, r2):
    a, b = min(r1), max(r1)
    c, d = min(r2), max(r2)
    start = min(a, c)
    end = min(b, d)
    return (start, end) if start <= end else None


def get_unmapped_ranges(seed_ranges, used_ranges):
    # for each used range, subtract the intersection from the seed range
    print(f"GUR-> Seed ranges: {seed_ranges}")
    print(f"GUR-> Used ranges: {used_ranges}")
    seed_ranges = sorted(set(seed_ranges))
    used_ranges = sorted(set(used_ranges))
    for used_range in used_ranges:
        new_seed_ranges = []
        for seed_range in seed_ranges:
            if intersection := range_intersection(seed_range, used_range):
                subtraction = range_difference(seed_range, intersection)
                new_seed_ranges.append(subtraction)
            else:
                new_seed_ranges.append(seed_range)
        seed_ranges = new_seed_ranges

    return sorted(set(seed_ranges) - set(used_ranges))


def string_of_numbers_to_list(line):
    return list(map(int, re.sub(" +", " ", line).strip().split(" ")))


if __name__ == "__main__":
    puzzle = read_puzzle()
    print(solve_puzzle(puzzle))
