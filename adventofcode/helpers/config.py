import datetime
import os
from pathlib import Path


_current_dir = Path(os.path.dirname(__file__))
TEMPLATES_DIR = _current_dir / ".." / "_templates"
SOLUTIONS_DIR = _current_dir / ".." / f"_{datetime.datetime.today().year}" / "solutions"