# HELPER FUNCTIONS USED IN ALL DAYS
from bitstring import BitArray


def read_input(filename=None, as_int=None, split_on=None):
    """
    Read the input file into a list of rows
    :param filename: The name of the input file, defaults to ./input
    :param as_int:  If true, convert each row into an int. Defaults to true
    :param split_on: String to split on. Defaults to \n
    :return: List[Any] Rows
    """
    filename = filename or "./input"
    as_int = True if as_int is None else as_int
    split_on = split_on or "\n"

    rows = open(filename, "r").read().split(split_on)
    # If split on \n, del last: Input has newline at end
    if split_on == "\n":
        del rows[-1]
    if as_int:
        rows = [int(i) if not i == "" else 0 for i in rows]
    return rows


def bit_list_to_int(l):
    """
    List of bits to decimal value
    :param l:
    :return:
    """
    return BitArray(l).uint
