import argparse
import os
import logging
logging.basicConfig(level = logging.INFO)

def create_file(day: int):
    """
    Create the file for a day:
    - Read template
    - Replace {day} with the value of day
    - Save to solutions/{day}.py
    """
    source_file = 'day.py.template'
    with open(source_file, 'r') as f:
        source = f.read()
    source = source.replace("{day}", str(day))
    destination_file = f'solutions/{day:02d}.py'
    if os.path.exists(destination_file):
        logging.error(f'File {destination_file} not created, as it yet exists')
        return
    with open(destination_file, 'x') as f:
        f.write(source)
    logging.info(f'File {destination_file} created')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='CreateDayToImplement',
        description='Generates a python file with boilerplate to solve a day'
    )
    parser.add_argument('-d', '--day', type=int, required=True)
    args = parser.parse_args()
    create_file(args.day)

