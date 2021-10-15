"""
paths to parsers, data is declared at here.
"""
from pathlib import Path
from os import path

# The directories
PACKAGE_ROOT = Path(__file__).resolve().parent.parent.__str__()
DATA_DIR = path.join(PACKAGE_ROOT, "data")
