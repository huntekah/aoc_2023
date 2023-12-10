from util.process_input import read_puzzle

def solve_puzzle(puzzle):
    s_location = find_s(puzzle)
    pipe_length = walk_the_pipes(puzzle, s_location)
    return pipe_length / 2

def find_s(puzzle):
    for i,row in enumerate(puzzle):
        if "S" in row:
            return i,row.index("S")

def walk_the_pipes(puzzle, s_location):
    steps = 1

    next_pipe = find_next_pipe(puzzle, s_location)
    while True:
        next_pipe = find_next_pipe(puzzle, next_pipe) # maybe stroe last two steps, not to repeat last step?
        if next_pipe == s_location:
            break
        steps +=1
    return steps
def find_next_pipe(puzzle, location):
    # We are at starting point S
    if puzzle[location[0]][location[1]] == "S":
        if puzzle[location[0]][location[1]]:
            # check if this is a valid pipe
            pass

if __name__ == "__main__":
    puzzle = read_puzzle("small_input.txt")
    # puzzle = read_puzzle()
    print(solve_puzzle(puzzle))
