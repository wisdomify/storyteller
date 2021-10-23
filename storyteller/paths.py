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
GK_DIR = path.join(CORPORA_DIR, "gk")  # 일반상식
SC_DIR = path.join(CORPORA_DIR, "sc")  # 감성대화
MR_DIR = path.join(CORPORA_DIR, "mr")  # 기계독해
DS_DIR = path.join(CORPORA_DIR, 'ds')  # 문서요약 - not prepared yet.


# test data
WISDOM2EG_GOLD_TSV = path.join(DATA_DIR, "wisdom2eg_gold.tsv")

