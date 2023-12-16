from util.process_input import read_puzzle

def solve_puzzle(puzzle):
    s_location = find_s(puzzle)
    # substitute_s_with_pipe(puzzle, s_location)
    pipe_length = walk_the_pipes(puzzle, s_location)
    return pipe_length / 2

def find_s(puzzle):
    for i,row in enumerate(puzzle):
        if "S" in row:
            print("FOUND S", (i, row.index("S")))
            return i,row.index("S")

# def substitute_s_with_pipe(puzzle, s_location):

def walk_the_pipes(puzzle, s_location):
    steps = 1

    current_pipe = s_location
    next_pipe = find_next_pipe(puzzle, current_pipe, None)
    print("FOUND FIRST PIPE!", next_pipe)
    while True:
        print("STEPS", steps, steps/2)
        # print(f"Walking from {current_pipe} to  {next_pipe}")
        current_pipe, next_pipe = next_pipe, find_next_pipe(puzzle, next_pipe, current_pipe) # maybe stroe last two steps, not to repeat last step?
        # show_puzzle_fragment(puzzle, [current_pipe[0], next_pipe[0]], [current_pipe[1], next_pipe[1]])
        # show_location(puzzle, next_pipe)
        steps +=1
        if next_pipe == s_location:
            print(f"FOUND S AGAIN {current_pipe},{next_pipe}")
            break
        # current_pipe = next_pipe
        if steps > 200000:
            break
    return steps
def find_next_pipe(puzzle, current_pipe, last_pipe) -> tuple:
    if last_pipe is None and puzzle[current_pipe[0]][current_pipe[1]] == "S":
        print("S")
        # Look for Possible pipes around S
        for i,j in [(0,1),(1,0),(0,-1),(-1,0)]: # right, down, left, up
            next_pipe = (current_pipe[0]+i,current_pipe[1]+j)
            if min(next_pipe) >= 0 and max(next_pipe) < len(puzzle) and is_connected(puzzle, current_pipe, next_pipe):
                print(f"found {next_pipe}",
                      puzzle[current_pipe[0] + i][current_pipe[1] + j])
                return next_pipe
    else:
        # print("FINDING NEXT PIPE, after s / None")
        # Look for Possible pipes around current pipe
        # possible_pipes = []
        # print("steps",get_steps(puzzle,current_pipe))
        for i,j in get_steps(puzzle,current_pipe):
        # for i,j in [(0,1),(1,0),(0,-1),(-1,0)]: # right, down, left, up
            next_pipe = (current_pipe[0]+i,current_pipe[1]+j)
            if next_pipe == last_pipe:
                continue
            # if min(next_pipe) >= 0 and max(next_pipe) < len(puzzle) and is_connected(puzzle, current_pipe, next_pipe):
            #     show_puzzle_fragment(puzzle, [current_pipe[0], next_pipe[0]], [current_pipe[1], next_pipe[1]])
            #     return next_pipe
            # if puzzle[next_pipe[0]][next_pipe[1]] == "S":
            return next_pipe
    raise Exception("No next pipe found")

def is_connected(puzzle, current_pipe, next_pipe) -> bool:
    """| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has."""
    # print(f"Checking {current_pipe} -> {next_pipe}")
    # show_puzzle_fragment(puzzle, [current_pipe[0], next_pipe[0]], [current_pipe[1], next_pipe[1]])
    # print(f"{puzzle[current_pipe[0]][current_pipe[1]]} -> {puzzle[next_pipe[0]][next_pipe[1]]}")
    if next_pipe is None:
            return False
    if next_pipe == (current_pipe[0]-1, current_pipe[1]) and puzzle[next_pipe[0]][next_pipe[1]] in "|F7":
        return True
    if next_pipe == (current_pipe[0]+1, current_pipe[1]) and puzzle[next_pipe[0]][next_pipe[1]] in "|LJ":
        return True
    if next_pipe == (current_pipe[0], current_pipe[1]-1) and puzzle[next_pipe[0]][next_pipe[1]] in "-LF":
        return True
    if next_pipe == (current_pipe[0], current_pipe[1]+1) and puzzle[next_pipe[0]][next_pipe[1]] in "-J7":
        return True
    return False

def show_puzzle_fragment(puzzle, rows, columns):
    print("Showing puzzle fragment")
    print("\n".join([f"{min(rows) + r}: " + row[min(columns):max(columns)+1] for r,row in enumerate(puzzle[
          min(rows):max(rows)+1
          ])])
          )

def show_location(puzzle, location):
    for r, row in enumerate(puzzle):
        for c, col in enumerate(row):
            if (r,c) == location:
                print("□", end="")
            else:
                print(col, end="")
        print()

def get_steps(puzzle, current_pipe):
    """| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has."""
    steps = []
    current_pipe_symbol = puzzle[current_pipe[0]][current_pipe[1]]
    # [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # right, down, left, up
    right = (0,1)
    down = (1,0)
    left = (0,-1)
    up = (-1,0)
    if current_pipe_symbol == "-":
        steps = [right,left]
    elif current_pipe_symbol == "|":
        steps = [up,down]
    elif current_pipe_symbol == "L":
        steps = [right,up]
    elif current_pipe_symbol == "J":
        steps = [left,up]
    elif current_pipe_symbol == "7":
        steps = [left,down]
    elif current_pipe_symbol == "F":
        steps = [right,down]
    elif current_pipe_symbol == "S":
        steps = [right,down,left,up]

    return steps

if __name__ == "__main__":
    # puzzle = read_puzzle("small_input2.txt")
    puzzle = read_puzzle("input.txt")
    # puzzle = read_puzzle()
    print(solve_puzzle(puzzle))
