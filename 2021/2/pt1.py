from helpers import read_input

rows = read_input(as_int=False)
h = 0
d = 0
for r in rows:
    val = int(r[-1])
    if 'forward' in r:
        h += val
    if 'up' in r:
        d -= val
    if 'down' in r:
        d += val
print(h * d)