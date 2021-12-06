from helpers import read_input

fish = read_input("input", split_on=',')

N_DAYS = 80

# Indexed on n_days_left. Value is the number of fish at day=0 as a result when having
# having 1 fish at value=0 and n_days_left=index
cache = {}


def get_val(n_days_left, parent_val):
    # Convert to parent_val = 0, which will be after parent_val days
    n_days_left -= parent_val
    # If no days left, will result in 1 fish
    if n_days_left <= 0:
        return 1
    # If previously computed, don't recompute
    if n_days_left in cache:
        return cache[n_days_left]
    # Next day: new child of 8, parent of 6
    n_days_left -= 1
    child_val = 8
    parent_val = 6
    # Result is sum of child and parent results
    result = get_val(n_days_left, parent_val) + get_val(n_days_left, child_val)
    # Save in cache
    cache[n_days_left + 1] = result
    return result


# For each fish, compute the total fish at day  = 0, sum
result = sum(get_val(N_DAYS, f) for f in fish)
print(result)
