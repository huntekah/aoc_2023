from util.process_input import read_puzzle

taken_steps = []

# new type Directions which is list of binary numbers
Directions = list[int]
# Nodes is a Dict with two nodes like node['AAA'] = ['BBB', 'CCC']
Nodes = dict[str, list[str]]
def solve_puzzle(puzzle):
    directions, nodes = transform_puzzle(puzzle)
    result = traverse_graph(directions, nodes, "AAA", 0)
    return result

def transform_puzzle(puzzle) -> tuple[Directions, Nodes]:
    directions: Directions = letters_to_directions(puzzle[0])
    nodes: Nodes = {}
    for line in puzzle[1:]:
        if line.strip() == "":
            continue
        else:
            node, children = read_node(line)
            nodes[node] = children
    return directions, nodes

def letters_to_directions(line: str) -> Directions:
    # 0 means L and 1 means R
    return [0 if c == "L" else 1 for c in line]

def read_node(line: str) -> tuple[str, list[str]]:
    # read line like "AAA = (BBB, CCC)" to tuple("AAA", ["BBB", "CCC"])
    node, children = line.split("=")
    node = node.strip()
    children = children.strip()[1:-1].split(",")
    children = [child.strip() for child in children]
    return node, children

def traverse_graph(directions: Directions, nodes: Nodes, node: str, steps: int) -> int:
    if node == "ZZZ":
        return steps
    next_node = nodes[node][directions[steps % len(directions)]]
    return traverse_graph(directions, nodes, next_node, steps + 1)


if __name__ == "__main__":
    SMALL_INPUT = False
    if SMALL_INPUT:
        puzzle = read_puzzle("small_input.txt")
        print(solve_puzzle(puzzle))
        assert 6 == solve_puzzle(puzzle)
    else:
        puzzle = read_puzzle("input.txt")
        print(solve_puzzle(puzzle))
