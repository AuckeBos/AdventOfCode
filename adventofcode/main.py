import datetime
import logging
import os
import subprocess
import click
from adventofcode.helpers.config import TEMPLATE_VERSION, TEMPLATES_DIR, solutions_dir
# Set debug level to info
logging.basicConfig(level=logging.INFO)



@click.group
def cli():
    """
    Main cli
    """
    
def create_file(year: int, day: int) -> str:
    """
    Create the file for a day:
    - Read template
    - Replace {day} with the value of day
    - Save to solutions/{day}.py
    """
    source_file = TEMPLATES_DIR / "day.py.template"
    with open(source_file, 'r', encoding='utf-8') as f:
        source = f.read()
    source = source.replace("{day}", str(day))
    source = source.replace("{year}", str(year))
    source = source.replace("{template_version}", TEMPLATE_VERSION)
    destination_file = solutions_dir(year) / f"{day:02d}.py"
    if os.path.exists(destination_file):
        logging.info('File %s not created, as it yet exists', destination_file)
    else:
        with open(destination_file, 'x', encoding='utf-8') as f:
            f.write(source)
        logging.info('File %s created', destination_file)
    return destination_file


@cli.command()
@click.option(
    "-y",
    "--year",
    type=int,
    required=False,
    default=datetime.datetime.today().year,
    help="The year to create a file for",
)
@click.option(
    "-d",
    "--day",
    type=int,
    required=datetime.datetime.today().month != 12,
    default=datetime.datetime.today().day if datetime.datetime.today().month == 12 else None,
    help="The day to create a file for",
)
def start(year: int, day: int):
    """
    Start a day. Ie create the file for the day, and open it in VS Code
    """
    path = create_file(year, day)
    os.system(f"code -r {path}")