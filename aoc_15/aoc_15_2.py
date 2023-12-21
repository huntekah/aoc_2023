import inspect
import re
from functools import cache
from itertools import product
from typing import Optional

from tqdm import tqdm

Value = tuple[str, int]
Box = list[Value]  # like [('xy',2)]
Bbox = list[Box]  # like [[('rn',1),('cm',2)],[],[],[('ot',7),('ab',5),('pc',6)]]


def solve_puzzle(puzzle) -> int:
    bbox: Bbox = [
        [] for _ in range(256)
    ]  # like [[('xy',2)],[],[],[('ot',7),('ab',5),('pc',6)]]
    for step in tqdm(puzzle):

        if "=" in step:
            l, v = step.split("=")
            h = hash_step(l)
            bbox = add_label_to_bbox(bbox, h, l, int(v))
            # print(f"{l=} => {hash_step(l)=} -> {v=}")
        elif "-" in step:
            l = step.split("-")[0]
            bbox = remove_label_from_bbox(bbox, l)
            # print(f"{l=} => {hash_step(l)=}")
        print(f"After {repr(step)}:")
        show_bbox(bbox)
    return count_score(bbox)


def count_score(bbox: Bbox) -> int:
    """One plus the box number of the lens in question.
    The slot number of the lens within the box: 1 for the first lens, 2 for the second lens, and so on.
    The focal length of the lens.

    At the end of the above example, the focusing power of each lens is as follows:

    rn: 1 (box 0) * 1 (first slot) * 1 (focal length) = 1
    cm: 1 (box 0) * 2 (second slot) * 2 (focal length) = 4
    ot: 4 (box 3) * 1 (first slot) * 7 (focal length) = 28
    ab: 4 (box 3) * 2 (second slot) * 5 (focal length) = 40
    pc: 4 (box 3) * 3 (third slot) * 6 (focal length) = 72"""
    s = 0
    print("Counting score")
    for i, box in enumerate(bbox, 1):
        if len(box) == 0:
            continue
        print(f"{i=}")
        for j, (l, v) in enumerate(box, 1):
            s += i * j * v
            print(f"\t- {l}: {i=} * {j=} * {v=} => {s=}")
    return s


def add_label_to_bbox(bbox: Bbox, h: int, l: str, v: int) -> Bbox:
    if l == "ot" and v == 7:
        print("debug")
    loc = _find_in_bbox(bbox, h, l)
    if loc is not None:
        # update value
        bbox[h][loc] = (l, v)
        return bbox
    else:
        # add a new value
        bbox[h].append((l, v))
        return bbox


def _find_in_bbox(bbox: Bbox, h: int, l: str) -> Optional[int]:
    return _find_in_box(bbox[h], l)


def remove_label_from_bbox(bbox: Bbox, label: str) -> Bbox:
    h = hash_step(label)
    # if _is_in_box(bbox[h], label):
    #     bbox[h] = _remove(bbox[h], label)
    # return bbox
    return (
        bbox[:h]
        + [_remove(bbox[h], label) if _is_in_box(bbox[h], label) else bbox[h]]
        + bbox[h + 1 :]
    )
    # return [box if not _is_in_box(box,label) else _remove(box,label) for box in bbox]


def _remove(box: Box, label: str) -> Box:
    new_box = [e for e in box if e[0] != label]
    return new_box


def _is_in_box(box: Box, label: str) -> bool:
    return any([b[0] == label for b in box])


def _find_in_box(box: Box, label: str) -> Optional[int]:
    for i, b in enumerate(box):
        if b[0] == label:
            return i
    return None


def show_bbox(bbox: Bbox) -> None:
    for i, box in enumerate(bbox):
        if len(box) == 0:
            continue
        print(f"Box {i}:", end="")
        for (l, v) in box:
            print(f" [{l} {v}]", end="")
        print()
    print()


def hash_step(s: str) -> int:
    """Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256."""
    v = 0
    for c in s:
        v = (v + ord(c)) * 17 % 256
    return v


def read_puzzle(filename: str):
    return [a.strip() for a in open(filename).read().split(",")]


if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle = read_puzzle("small_input.txt")
        result = solve_puzzle(puzzle)
        print(result)
        assert 145 == result
    else:
        puzzle = read_puzzle("input.txt")
        solution = solve_puzzle(puzzle)
        assert 258826 == solution
        print(solution)
