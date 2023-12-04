import datetime
import os
from pathlib import Path


_current_dir = Path(os.path.dirname(__file__))
TEMPLATE_VERSION = "v20231204"
TEMPLATES_DIR = _current_dir / ".." / "_templates" / TEMPLATE_VERSION
SOLUTIONS_DIR = _current_dir / ".." / f"_{datetime.datetime.today().year}" / "solutions"