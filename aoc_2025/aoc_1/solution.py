from pathlib import Path
from util.process_input import read_puzzle, Puzzle

class Solution():
    def __call__(self):
        input_path = Path(__file__).parent / "input.txt"
        problem = read_puzzle(str(input_path))
        dial = 50
        zeros = 0
        for turn in problem:
            direction = 1 if turn[0] == 'R' else -1
            value = int(turn[1:])
            dial += direction * value
            dial %= 100
            if dial == 0:
                zeros += 1
        print(zeros)

Solution()()
