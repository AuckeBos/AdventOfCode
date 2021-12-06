from board import Board

from helpers import read_input

PART = 1

rows = read_input(as_int=False)

vals = [int(v) for v in rows.pop(0).split(",")]
rows.pop(0)
boards = []

while rows:
    # Loop over each item in each row. But first: string and replace "  " with " "
    board = [
        int(item)
        for sublist in rows[:5]
        for item in sublist.strip().replace("  ", " ").split(" ")
    ]
    del rows[:6]
    boards.append(Board(board))

done = []
for val in vals:
    for i, board in enumerate(boards):
        if i in done:
            continue
        score = board.tick(val)
        if score:
            # PT1: stop on first
            if PART == 1:
                print(score)
                exit()
            done.append(i)
            # PT2: If all done, print last
            if len(done) == len(boards):
                print(score)
                exit()
