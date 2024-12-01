from aocd.models import Puzzle

# Cache of get_val
cache = {}


def get_val(n_days_left: int, val: int):
    """
    Get the number of fish after n_days_left if we would have 1 fish with value val
    :param n_days_left: n days left
    :param val: cur
    :return:
    """
    # Convert to val = 0, which will be after val days
    n_days_left -= val
    # If no days left, will result in 1 fish
    if n_days_left <= 0:
        return 1
    if n_days_left in cache:
        return cache[n_days_left]
    # Next day: new child of puzzle_8, parent of 6
    n_days_left -= 1
    child_val = 8
    parent_val = 6
    # Result is sum of child and parent results
    result = get_val(n_days_left, parent_val) + get_val(n_days_left, child_val)
    cache[n_days_left + 1] = result
    return result


puzzle = Puzzle(year=2021, day=6)
fish = [int(f) for f in puzzle.input_data.split(",")]

puzzle.answer_a = sum(get_val(80, f) for f in fish)
puzzle.answer_b = sum(get_val(256, f) for f in fish)
