import inspect
from tqdm import tqdm

# from util.process_input import Puzzle, read_puzzle, string_of_numbers_to_list
from util.process_input import Puzzle, string_of_numbers_to_list
import re
from itertools import product
from functools import cache
from collections import defaultdict
from typing import Optional
from typing import Iterator
### Puzzle description ###
# find mirror reflections of text input, either row or column wise:
# 123456789
#     ><
# #.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.
#     ><
# 123456789
#
# or
# 1 #...##..# 1
# 2 #....#..# 2
# 3 ..##..### 3
# 4v#####.##.v4
# 5^#####.##.^5
# 6 ..##..### 6
# 7 #....#..# 7
### PUZZLE DESCRIPTION END ###

Pattern = list[str]
Patterns = list[Pattern]

def solve_puzzle(puzzle: Patterns) -> int:
    records: Patterns = puzzle

    row_mirrors = 0
    column_mirrors = 0
    for record in records:
        print("\n".join(record))

        # original_mirror : tuple[list[int],list[int]] = get_original_mirrors_from_record(record)
        r,c = find_one_off_reflections(record)
        row_mirrors += r
        column_mirrors += c
        continue
        print(original_mirror)
        used_row_mirrors = [*original_mirror[0]]
        used_column_mirrors = [*original_mirror[1]]
        # print("len-> ",len([a for a in get_all_smudge_substitutions(record)]))
        for tmp_record in get_all_smudge_substitutions(record):
            # print(tmp_record)
            # if tmp_record[1] != ".##.###......###.":
            #     continue
                # print("xxxx")
                # print("\n".join(tmp_record))
            # print("M\n" + "\n".join(tmp_record))
            if new_mirror := get_mirror_from_record(tmp_record, original_mirror):
                # if new_mirror == original_mirror:
                    # print(f"\tNot using {new_mirror=}, {original_mirror=}")
                    # continue
                # print(f"\t{new_mirror=},\n\t{original_mirror=},\n\t{'different' if new_mirror != original_mirror else 'same'}")
                new_rows = list(set(new_mirror[0]) - set(used_row_mirrors))
                new_columns = list(set(new_mirror[1]) - set(used_column_mirrors))
                row_mirrors += sum(new_rows)
                column_mirrors += sum(new_columns)
                used_row_mirrors.extend(new_rows)
                used_column_mirrors.extend(new_columns)
                # if new_mirror[0] in used_row_mirrors:
                    # print(f"\t\t{new_mirror[0]} already used")
                    # pass
                # else:
                #     used_row_mirrors.append(new_mirror[0])
                #     row_mirrors += new_mirror[0]
                # if new_mirror[1] in used_column_mirrors:
                    # print(f"\t\t{new_mirror[1]} already used")
                    # pass
                # else:
                #     used_column_mirrors.append(new_mirror[1])
                #     column_mirrors += new_mirror[1]
                # row_mirrors += new_mirror[0]
                # column_mirrors += new_mirror[1]
                # if new_mirror[0] == "row":
                #     row_mirrors += new_mirror[1]
                #     print("_v_")
                #     print("\n".join(tmp_record))
                #     print(f"ROW MIRROR FOUND AT {new_mirror[1]}")
                #     # break
                # elif new_mirror[0] == "col":
                #     column_mirrors += new_mirror[1]
                #     print("_v_")
                #     print("\n".join(tmp_record))
                #     print(f"COLUMN MIRROR FOUND AT {new_mirror[1]}")
                    # break
        print("______________________")
    print(f"{row_mirrors=} {column_mirrors=}")
    return row_mirrors,column_mirrors #, 100 * row_mirrors + column_mirrors

def find_one_off_reflections(record: Pattern) -> Optional[int]:
    row_reflections = find_one_off_reflection(record)
    col_reflections = find_one_off_reflection(list(zip(*record)))
    return row_reflections, col_reflections

def find_one_off_reflection(record: Pattern) -> Optional[int]:
    for i in range(1, len(record[0])):
        split = min(i, len(record[0]) - i)
        num_differences = 0
        for row in record:
            for l, r in zip(row[i - split:i], row[i:i + split][::-1]):
                if l != r:
                    num_differences += 1
            if num_differences > 1:
                break
        if num_differences == 1:
            return i
    return 0

# def get_new_mirror_from_record(record: Pattern, old_mirror: tuple[str,int]) -> Optional[tuple[str, int]]:
#     new_mirror = get_mirror_from_record(record)
#     if new_mirror == old_mirror:
#         return None
#     return new_mirror
def get_original_mirrors_from_record(record: Pattern) -> tuple[list,list]:
    if r := get_mirror_from_record(record):
        return r
    return ([],[])
def get_mirror_from_record(record: Pattern, old_mirrors: tuple[list,list] = (None, None)) -> tuple[list, list]:
    hashed_rows = get_hashed_rows(record)
    hashed_columns = get_hashed_columns(record)
    mirror_row_locations = []
    mirror_col_locations = []
    for mirror_location in find_mirror_location_by_hash(hashed_rows):
        if old_mirrors and mirror_location not in old_mirrors[0]:
            mirror_row_locations.append(mirror_location)
    for mirror_location in find_mirror_location_by_hash(hashed_columns):
        if old_mirrors and mirror_location not in old_mirrors[1]:
            mirror_col_locations.append(mirror_location)
    if len(mirror_row_locations) == 0 and len(mirror_col_locations) == 0:
        return None
    return mirror_row_locations, mirror_col_locations
    # print("NO MIRROR FOUND")
    # print("\n".join(record))
    # print("_^_")
def get_all_smudge_substitutions(record: Pattern) -> list[Pattern]:
    # record = record.copy()
    for i,row in enumerate(record):
        for j,char in enumerate(row):
            if char == ".":
                yield record[:i] + [row[:j] + "#" + row[j+1:]] + record[i+1:]
            else:
                yield record[:i] + [row[:j] + "." + row[j+1:]] + record[i+1:]

def get_hashed_rows(record: Pattern) -> dict[int, list[int]]:
    hashed_rows = defaultdict(list)
    for i,row in enumerate(record,1):
        # hashed_rows[hash(row)].append(i)
        hashed_rows[row].append(i)
    return hashed_rows

def get_hashed_columns(record: Pattern) -> dict[int, list[int]]:
    hashed_columns = defaultdict(list)
    for i,column in enumerate(zip(*record),1):
        # hashed_columns[hash(column)].append(i)
        hashed_columns[column].append(i)
    return hashed_columns

def find_mirror_location_by_hash(hashed_rows: dict[int, list[int]]) -> Iterator[int]:
    # find all middles
    # for all middles, make a list of tuples of all matching row indices, if it would be a mirror
    # iterate through hashed_rows, and delete tuple from middles_list, if it is in there
    # if middles_list is empty, we found a mirror
    middles_list = []

    for row_hash, row_indices in hashed_rows.items():
        possible_mirrors_middles = [(row_indices[i],row_indices[i+1]) for i in range(len(row_indices) - 1) if abs(row_indices[i] - row_indices[i + 1]) == 1]
        middles_list.extend(possible_mirrors_middles)

    # print(hashed_rows.values())
    last_row = max(row_id for row_indices in hashed_rows.values() for row_id in row_indices)
    for try_middle in middles_list:
        a = try_middle[0]
        b = try_middle[1]
        is_middle = False
        while a >= 1 and b <= last_row:
            is_middle = False
            for row_indices in hashed_rows.values():
                if a in row_indices and b in row_indices:
                    is_middle = True
                    break
            if not is_middle:
                break
            a -= 1
            b += 1
        if is_middle:
            # print(f"try: {try_middle}")
            yield try_middle[0]

    # return None
def read_puzzle(filename: str) -> Patterns:
    with open(filename) as file:
        records = [pattern.strip().split("\n")  for pattern in file.read().strip().split("\n\n")]
        return records


def correct_solution_from_savbell(puzzle):
    # maps = [[list(row) for row in m] for m in [m.split('\n') for m in q[13].strip().split('\n\n')]]
    maps = [[list(row) for row in m] for m in puzzle]

    def find_one_off_reflection(map):
        for col in range(1, len(map[0])):
            split = min(col, len(map[0]) - col)
            num_differences = 0
            for row in map:
                for l, r in zip(row[col - split:col], row[col:col + split][::-1]):
                    if l != r:
                        num_differences += 1
                if num_differences > 1:
                    break
            if num_differences == 1:
                return col

    columns = 0
    rows = 0
    for m in maps:
        vertical = find_one_off_reflection(m)
        horizontal = find_one_off_reflection(list(zip(*m)))
        columns += vertical if vertical else 0
        rows += horizontal if horizontal else 0
    return rows, columns

def f(p,s=1):
    for i in range(len(p)):
        if sum(c != d for l,m in zip(p[i-1::-1], p[i:])
                      for c,d in zip(l, m)) == s: return i
    else: return 0

def generate_random_mirror(size):
    from random import choice
    return ["".join([choice(".#") for _ in range(size)]) for _ in range(size)]

if __name__ == "__main__":
    diff = False
    n = 0
    while not diff:
        print(f"({n})\t" + "X"*100)
        n+=1
        puzzle = [generate_random_mirror(4)]
        print("          1111111")
        print("12345667890123456")
        puzzle = read_puzzle("input.txt")
        my_result = solve_puzzle(puzzle)
        savbell_result = correct_solution_from_savbell(puzzle)
        topaz_result = (f(puzzle), f([zip(*puzzle)]))
        print(f"{my_result=}")
        print(f"{savbell_result=}")
        print(f"{topaz_result=}")
        print(f"{my_result[0] * 100 + my_result[1] = }")
        break
        if my_result != savbell_result:
            print("(row, col)")
            # print(f"{my_result=}")
            # print(f"{savbell_result=}")
            diff = True
    exit()
    SMALL = True
    if SMALL:
        puzzle: Patterns = read_puzzle("small_input3.txt")
        result = solve_puzzle(puzzle)
        print(result)
        assert 1400 == result
    else:
        puzzle = read_puzzle("input.txt")
        print(solve_puzzle(puzzle))

# not 290, 343
