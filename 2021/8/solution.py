from helpers import read_input
from line import Line

# PT1: Cost 1 per step
# PT2: Cum cost per step
PART = 2
line_inputs = read_input("input", as_int=False)
lines = [Line(input) for input in line_inputs]

if PART == 1:
    digits_to_select = [d for l in lines for d in l.outputs if d.is_simple_digit()]
    n_digits = len(digits_to_select)
    print(n_digits)
elif PART == 2:
    outputs = [line.compute_output() for line in lines]
    result = sum(outputs)
    print(result)

