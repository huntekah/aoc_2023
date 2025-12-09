from pathlib import Path
from util.process_input import read_puzzle, Puzzle

class Solution():
    def __call__(self):
        input_path = Path(__file__).parent / "input.txt"
        # input_path = Path(__file__).parent / "example.txt"
        problem = read_puzzle(str(input_path))
        dial = 50
        zeros = 0
        for turn in problem:
            direction = 1 if turn[0] == 'R' else -1
            value = int(turn[1:])
            prev_dial = dial
            dial += direction * value

            # Count multiples of 100 crossed
            if direction == 1:  # right rotation
                # Count multiples of 100 in (prev_dial, dial]
                zeros += dial // 100 - prev_dial // 100
            else:  # left rotation
                # Count multiples of 100 in [dial, prev_dial)
                zeros += (prev_dial - 1) // 100 - (dial - 1) // 100

            dial %= 100

        print(zeros)

Solution()()
