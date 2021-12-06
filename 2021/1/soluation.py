from helpers import read_input

# PT1: 1, PT2: 3
WINDOW_SIZE = 3
rows = read_input()
count = 0
for i in range(1, len(rows)):
    curr_sum = sum(rows[i:i+WINDOW_SIZE])
    prev_sum = sum(rows[i-1:i+WINDOW_SIZE - 1])
    if curr_sum > prev_sum:
        count += 1
print(count)