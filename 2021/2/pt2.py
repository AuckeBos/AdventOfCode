from helpers import read_input

rows = read_input(as_int=False)
h = 0
d = 0
a = 0
for r in rows:
    val = int(r[-1])
    if 'forward' in r:
        h += val
        d += a * val
    if 'up' in r:
        a -= val
    if 'down' in r:
        a += val
print(h * d)