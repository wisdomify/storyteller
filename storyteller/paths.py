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
NEWS_DIR = path.join(CORPORA_DIR, "news")  # 뉴스데이터

# wandb - related
WANDB_DIR = path.join(DATA_DIR, "wandb")
ARTIFACTS_DIR = path.join(WANDB_DIR, "artifacts")
# --- wisdom2def --- #
WISDOM2DEF_DIR = path.join(ARTIFACTS_DIR, "wisdom2def")
WISDOM2DEF_RAW_TSV = path.join(WISDOM2DEF_DIR, "wisdom2def_raw.tsv")
WISDOM2DEF_TSV = path.join(WISDOM2DEF_DIR, "wisdom2def.tsv")
WISDOM2DEF_TRAIN_TSV = path.join(WISDOM2DEF_DIR, "wisdom2def_train.tsv")
WISDOM2DEF_VAL_TSV = path.join(WISDOM2DEF_DIR, "wisdom2def_val.tsv")
# --- wisdom2eg --- #
WISDOM2EG_DIR = path.join(ARTIFACTS_DIR, "wisdom2eg")
WISDOM2EG_RAW_TSV = path.join(WISDOM2EG_DIR, "wisdom2eg_raw.tsv")
WISDOM2EG_TSV = path.join(WISDOM2EG_DIR, "wisdom2eg.tsv")
WISDOM2EG_TRAIN_TSV = path.join(WISDOM2EG_DIR, "wisdom2eg_train.tsv")
WISDOM2EG_VAL_TSV = path.join(WISDOM2EG_DIR, "wisdom2eg_val.tsv")
# --- the test data to use --- #
WISDOMIFY_TEST_TSV = path.join(ARTIFACTS_DIR, "wisdomify_test.tsv")
# --- the wisdom vocabulary --- #
WISDOMS_TXT = path.join(ARTIFACTS_DIR, "wisdoms.txt")
