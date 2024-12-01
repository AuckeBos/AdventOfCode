from src._2022.puzzle_to_solve import PuzzleToSolve


class Puzzle10(PuzzleToSolve):
    @property
    def day(self) -> int:
        return 10

    @property
    def test_input(self) -> str:
        return """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

    @property
    def test_answer_a(self):
        return 13140

    @property
    def test_answer_b(self):
        return ''

    def compute_register_changes(self, input_: str):
        """
        Compute a list of register changes, based on a list of ops:
        - If op is noop, append 0 - register doesn't change
        - If op is add, extend [0, change]: Takes 2 cycles
        """
        operations = input_.split("\n")
        register_changes = []
        for op in operations:
            if op == 'noop':
                register_changes.append(0)
            elif op.startswith('addx'):
                change = int(op.split(" ")[1])
                register_changes.extend([0, change])
            else:
                raise Exception(f'Cannot parse operation {op}')
        return register_changes

    def a(self, input_: str):
        """
        Solve a):
        - Compute register changes
        - Find the set of computation points
        - For each point, compute the strength: The register changes until that point + 1
        - Sum the result
        """
        register_changes = self.compute_register_changes(input_)
        computation_points = [20 + i * 40 for i in range(len(register_changes) // 40)]
        signal_strenghts = []
        for p in computation_points:
            signal_strenghts.append(p * (sum(register_changes[:p - 1]) + 1))
        result = sum(signal_strenghts)
        return result

    def b(self, input_: str):
        """
        Solve b):
        - Compute register changes
        - Set crt post to 0 and xpos to 1
        - Loop over changes, for each change:
            - Check first if crt_pos is within the sprint (x-1 : x+1). If so, char is # (lit), else . (dark)
            - Increase X_pos and crt_pos mod 40
        - Change chars for better readability
        - Split into 6 lines, print each line
        - Ask the user to read the result, and input the 8 capital letters that should be read
        - Return user input
        """
        register_changes = self.compute_register_changes(input_)
        crt_pos = 0
        X_pos = 1
        result = ''
        for change in register_changes:
            if X_pos - 1 <= crt_pos <= X_pos + 1:
                char = '#'
            else:
                char = '.'
            result += char
            X_pos += change
            crt_pos = (crt_pos + 1) % 40
        result = result.replace('.', ' ').replace("#", '.')
        lines = [result[i:i + 40] for i in range(0, len(register_changes), 40)]
        for line in lines:
            print(line)
        # Manually read the output, and submit the result
        result = input("What 8 capital letters to you see (Submit empty string for test input)?")
        return result


puzzle = Puzzle10()
puzzle.solve()
