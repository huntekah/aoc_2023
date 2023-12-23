from collections import defaultdict
from functools import cache
from typing import Optional

from tqdm import tqdm

from util.process_input import Puzzle, read_puzzle

Location = tuple[int, int]
# binary 0 or 1 for each direction: up, right, down, left
UP = 0b0001  # 1
RIGHT = 0b0010  # 2
DOWN = 0b0100  # 4
LEFT = 0b1000  # 8
Directions = int
Field = tuple[str]
direction_to_location = {
    UP: lambda y, x: (y - 1, x),  # up
    RIGHT: lambda y, x: (y, x + 1),  # right
    DOWN: lambda y, x: (y + 1, x),  # down
    LEFT: lambda y, x: (y, x - 1),  # left
}


def solve_puzzle(puzzle: Puzzle) -> int:
    field = Field(puzzle)
    start: Location = (0, 0)
    stop: Location = (len(field) - 1, len(field[0]) - 1)
    c_min = 4
    c_max = 10
    distance = solve_with_djikstra(field, start, stop, c_min, c_max)
    return distance


def solve_with_djikstra(
    field: Field, start: Location, stop: Location, c_min: int, c_max: int
) -> int:
    """Solve with djikstra search. Distance in last direction cannot exceed c"""
    starting_score = 0  # int(field[start[0]][start[1]])
    active_nodes: dict[tuple[Location, Directions, int], int] = {
        (start, 0b0000, 0): starting_score
    }  # {(location, last_direction, disrtance_in_last_direction) : weight}
    used_nodes = {}
    # shortest_distance = None
    t = tqdm(total=1)
    # paths = {start:None} # {start: stop}

    while len(active_nodes) > 0:
        t.total = len(active_nodes)
        t.update()
        t.refresh()

        c_node = min(active_nodes, key=active_nodes.get)
        c_location = c_node[0]
        c_last_direction = c_node[1]
        c_dild = c_node[2]
        c_weight = active_nodes.pop(c_node)

        used_nodes[(c_location, c_last_direction, c_dild)] = c_weight
        # show_paths(used_nodes, field)

        if c_location == stop and c_dild >= c_min:
            # show_paths(used_nodes, field)
            return c_weight  # + int(field[-1][-1])
        # if shortest_distance and c_weight > shortest_distance:
        #     continue

        for direction in get_directions(c_last_direction, c_dild, c_min, c_max):
            new_location = direction_to_location[direction](*c_location)
            if not is_valid_location(field, new_location):
                continue

            new_weight = int(field[new_location[0]][new_location[1]]) + c_weight
            # print(new_weight)
            # if new_location == stop:
            #     if shortest_distance is None or c_weight < shortest_distance:
            #         shortest_distance = new_weight
            #     continue

            if c_last_direction == direction:
                new_dild = c_dild + 1
            else:
                new_dild = 1
            if (new_location, direction, new_dild) not in used_nodes:
                # Here we could optimize against direction and new_dild.
                if (new_location, direction, new_dild) in active_nodes:
                    if active_nodes[(new_location, direction, new_dild)] > new_weight:
                        active_nodes[(new_location, direction, new_dild)] = new_weight
                        # paths[new_location] = c_location
                else:
                    active_nodes[(new_location, direction, new_dild)] = new_weight
    return min([used_nodes[node] for node in used_nodes if node[0] == stop]) + int(
        field[-1][-1]
    )


@cache
def get_directions(
    last_direction: Directions, distance_in_last_direction: int, c_min: int, c_max: int
) -> set[Directions]:
    """Get all directions that are valid.
    if dild < c_min, you cannot turn.
    if dild >= c_max, you cannot go straight"""
    current_direction_to_next_direction = {
        UP: {UP, RIGHT, LEFT},
        RIGHT: {UP, RIGHT, DOWN},
        DOWN: {RIGHT, DOWN, LEFT},
        LEFT: {UP, DOWN, LEFT},
        0b0000: {UP, RIGHT, DOWN, LEFT},  # starting position has no last direction
    }
    if distance_in_last_direction < c_min:
        if last_direction == 0b0000:
            return current_direction_to_next_direction[last_direction]
        return {last_direction}
    elif distance_in_last_direction < c_max:
        return current_direction_to_next_direction[last_direction]
    else:
        return current_direction_to_next_direction[last_direction] - {last_direction}


def is_valid_location(field: Field, location: Location) -> bool:
    """Check if location is valid"""
    x, y = location
    return 0 <= x < len(field) and 0 <= y < len(field[0])


def show_paths(
    used_nodes: dict[tuple[Location, Directions, int], int], field: Field
) -> None:
    """Show paths in a field"""
    direction_to_arrow = {
        UP: "^",
        RIGHT: ">",
        DOWN: "v",
        LEFT: "<",
        0b0000: "S",
    }
    print("Field:")
    for i, row in enumerate(field):
        for j, symbol in enumerate(row):
            best_node = min(
                [node for node in used_nodes if node[0] == (i, j)],
                key=lambda node: used_nodes[node],
                default=None,
            )
            if best_node:
                print(direction_to_arrow[best_node[1]], end="")
            else:
                print(symbol, end="")
        print()
    print()


if __name__ == "__main__":
    SMALL = False
    if SMALL:
        puzzle = read_puzzle("small_input5.txt")
        result = solve_puzzle(puzzle)
        print(result)
        assert 102 == result
    else:
        puzzle = read_puzzle("input.txt")
        solution = solve_puzzle(puzzle)
        print(solution)
        assert 987 < solution

# 816 too low.
# 845 is ok
# 849 too high
