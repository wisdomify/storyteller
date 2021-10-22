"""
paths to parsers, data is declared at here.
"""
from pathlib import Path
from os import path

# The directories
ROOT_DIR = Path(__file__).resolve().parent.parent.__str__()
DATA_DIR = path.join(ROOT_DIR, "data")
CORPORA_DIR = path.join(DATA_DIR, "corpora")


# corpora
GK_DIR = path.join(CORPORA_DIR, "gk")
SC_DIR = path.join(CORPORA_DIR, "sc")
DS_DIR = path.join(CORPORA_DIR, 'ds')


# test data
WISDOM2EG_GOLD_TSV = path.join(DATA_DIR, "wisdom2eg_gold.tsv")

