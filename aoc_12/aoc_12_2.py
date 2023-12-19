import inspect
from tqdm import tqdm

from util.process_input import Puzzle, read_puzzle, string_of_numbers_to_list
import re
from itertools import product
from functools import cache
### Puzzle description ###

# In the giant field just outside, the springs are arranged into rows. For each row, the condition records show every spring and whether it is operational (.) or damaged (#). This is the part of the condition records that is itself damaged; for some springs, it is simply unknown (?) whether the spring is operational or damaged.
#
# However, the engineer that produced the condition records also duplicated some of this information in a different format! After the list of springs for a given row, the size of each contiguous group of damaged springs is listed in the order those groups appear in the row. This list always accounts for every damaged spring, and each number is the entire size of its contiguous group (that is, groups are always separated by at least one operational spring: #### would always be 4, never 2,2).
#
# So, condition records with no unknown spring conditions might look like this:
#
# #.#.### 1,1,3
# .#...#....###. 1,1,3
# .#.###.#.###### 1,3,1,6
# ####.#...#... 4,1,1
# #....######..#####. 1,6,5
# .###.##....# 3,2,1
# However, the condition records are partially damaged; some of the springs' conditions are actually unknown (?). For example:
#
# ???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1
# Equipped with this information, it is your job to figure out how many different arrangements of operational and broken springs fit the given criteria in each row.
#
# In the first line (???.### 1,1,3), there is exactly one way separate groups of one, one, and three broken springs (in that order) can appear in that row: the first three unknown springs must be broken, then operational, then broken (#.#), making the whole row #.#.###.
#
# The second line is more interesting: .??..??...?##. 1,1,3 could be a total of four different arrangements. The last ? must always be broken (to satisfy the final contiguous group of three broken springs), and each ?? must hide exactly one of the two broken springs. (Neither ?? could be both broken springs or they would form a single contiguous group of two; if that were true, the numbers afterward would have been 2,3 instead.) Since each ?? can either be #. or .#, there are four possible arrangements of springs.
#
# The last line is actually consistent with ten different arrangements! Because the first number is 3, the first and second ? must both be . (if either were #, the first number would have to be 4 or higher). However, the remaining run of unknown spring conditions have many different ways they could hold groups of two and one broken springs:
#
# ?###???????? 3,2,1
# .###.##.#...
# .###.##..#..
# .###.##...#.
# .###.##....#
# .###..##.#..
# .###..##..#.
# .###..##...#
# .###...##.#.
# .###...##..#
# .###....##.#
# In this example, the number of possible arrangements for each row is:
#
# ???.### 1,1,3 - 1 arrangement
# .??..??...?##. 1,1,3 - 4 arrangements
# ?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
# ????.#...#... 4,1,1 - 1 arrangement
# ????.######..#####. 1,6,5 - 4 arrangements
# ?###???????? 3,2,1 - 10 arrangements
# Adding all of the possible arrangement counts together produces a total of 21 arrangements.
#
# For each row, count all of the different arrangements of operational and broken springs that meet the given criteria. What is the sum of those counts?

### PUZZLE DESCRIPTION END ###

Records = list[str]
damaged = "#"
operational = "."
unknown = "?"

possible_could_bees = {}

def solve_puzzle(puzzle: Puzzle) -> int:
    records: Records = puzzle

    arrangements: list[int] = find_out_possible_arrangements_for_records(records)
    return sum(arrangements)

def find_out_possible_arrangements_for_records(records: Records) -> list[int]:
    arrangements: list[int] = []
    for record in tqdm(records):
        arrangements.append(find_out_possible_arrangements_for_record(record))
        # print(f"{arrangements=}")
    return arrangements


def find_out_possible_arrangements_for_record(record: str) -> int:
    # read both types of records
    normal: str = record.split(" ")[0]
    compressed: tuple[int] = tuple(map(int, record.split(" ")[1].split(",")))
    # multiply both times 5
    normal = "?".join([normal] * 5) + "." #additional dot at the end
    compressed = compressed*5
    # print(f"{normal=} {compressed=} {compress_record(normal)=}")
    n_arrangements = count_permutations(normal, compressed, 0)
    # print(n_arrangements)
    return n_arrangements
    # n_arrangements = 0
    # for arrangement in tqdm(get_all_possible_arrangements(normal)):
    #     if compress_record(arrangement) == compressed:
    #         n_arrangements += 1
    # # arrangements = find_arrangements_by_uncompression(normal, compressed)
    #
    # return n_arrangements

@cache
def count_permutations(normal, compressed, g_loc=0) -> int:
    if not normal:
        return not compressed and not g_loc
    results = 0
    arrangement_options = [operational, damaged] if normal[0] == unknown else [normal[0]]
    for arrangement in arrangement_options:
        if arrangement == damaged:
            results += count_permutations(normal[1:], compressed, g_loc +1)
        else:
            if g_loc >0:
                if compressed and compressed[0] == g_loc:
                    results += count_permutations(normal[1:], compressed[1:])
            else:
                results += count_permutations(normal[1:], compressed, g_loc)
    return results
def get_all_possible_arrangements(normal: str) -> list[str]:
    arrangement_options = []
    for char in normal:
        if char == unknown:
            arrangement_options.append([operational, damaged])
        else:
            arrangement_options.append([char])
    arrangements = product(*arrangement_options)
    for arrangement in arrangements:
        yield "".join(arrangement)

def compress_record(record: str) -> list[int]:
    # return compressed record
    # transform row like "#.#.###" to [1, 1, 3]
    # transform row like ".#...#....###." to [1, 1, 3]
    # transform row like ".#.###.#.######" to [1, 3, 1, 6]
    matches = re.findall(r"#+", record)
    compressed: list[int] = [len(match) for match in matches]
    return compressed

    #
    # last = None
    #
    # for char in record:
    #     if last != char and char == damaged:
    #         compressed.append(1)
    #     elif char == damaged:
    #         compressed[-1] += 1
    #     last = char
    # return compressed

def find_arrangements_by_uncompression(normal: str, compressed: list[int]) -> int:
    arrangements = 0
    for try_n in uncompress_record(compressed, len(normal)):
        print(f"{normal=} {try_n=}")
        if could_be_the_same_records(normal, try_n):
            arrangements += 1
    return arrangements


def uncompress_record(compressed: list[int], length: int) -> list[str]:
    # return all possible uncompressed records
    # transform [1, 1, 3] with len 6 to [".#.#.###", "#..#.###","#.#..###","#.#.###."]
    uncompressions = [simple_uncompress_record(compressed)]
    # print(uncompressions)
    while len(uncompressions[0]) < length:
        # print(uncompressions)
        uncompressions = uncompress_record_helper(uncompressions)
    return uncompressions

def uncompress_record_helper(uncompressions: list[str]) -> list[str]:
    new_uncompressions = []
    for uncompression in uncompressions:
        new_uncompressions.extend(insert_operational_near_other_operational(uncompression))
    return new_uncompressions

def simple_uncompress_record(compressed: list[int]) -> str:
    # return uncompressed record
    # transform [1, 1, 3] to "#.#.###"
    uncompressed = ""
    for i, n in enumerate(compressed):
        uncompressed += n * damaged + operational
    return uncompressed[:-1]
def could_be_the_same_records(normal: str, try_n: str) -> bool:
    if (normal, try_n) in possible_could_bees:
        return possible_could_bees[(normal, try_n)]
    for i, char in enumerate(normal):
        if char == unknown:
            continue
        if char != try_n[i]:
            possible_could_bees[(normal, try_n)] = False
            return False
    possible_could_bees[(normal, try_n)] = True
    return True

def insert_operational_near_other_operational(record: str) -> list[str]:
    # return all possible records with one more operational
    # transform "#.#.###" to [".#.#.###", "#..#.###","#.#..###","#.#.###."]
    new_records = []
    for i, char in enumerate(record):
        if char == operational:
            new_records.append(record[:i] + operational + record[i:])
    return new_records

if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle: Puzzle = read_puzzle("small_input.txt")
        result = solve_puzzle(puzzle)
        print(result)
        assert 21 == result
    else:
        puzzle = read_puzzle("input.txt")
        print(solve_puzzle(puzzle))


# ....1........
# .........2...
# 3............
# .............
# .............
# ........4....
# .5...........
# .#..........6
# .#...........
# .#...........
# .####....7...
# 8....9.......
