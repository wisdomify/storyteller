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
BS_DIR = path.join(CORPORA_DIR, "bs")  # 도서자료 요약
CVC_DIR = path.join(CORPORA_DIR, "cvc")  # 명령어 음성(소아, 유아)
DS_DIR = path.join(CORPORA_DIR, "ds")   # 문서요약 텍스트
SFC_DIR = path.join(CORPORA_DIR, "sfc")     # 전문분야 말뭉치
KESS_DIR = path.join(CORPORA_DIR, "kess")     # 한국어-영어 번역 말뭉치 (사회과학)
KJ_DIR = path.join(CORPORA_DIR, "kj")     # 한국어-일본어 번역 말뭉치
KCSS_DIR = path.join(CORPORA_DIR, "kcss")     # 한국어-중국어 번역 말뭉치 사회과학

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
