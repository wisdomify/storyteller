import pandas as pd
from typing import List
from storyteller.paths import WISDOMS_TXT, WISDOM2DEF_TSV, WISDOM2EG_TSV, WISDOM2DEF_RAW_TSV, WISDOM2EG_RAW_TSV
from dotenv import load_dotenv, find_dotenv
# init the environment

# this loads all the environment variable from .env to os.environ.
load_dotenv(dotenv_path=find_dotenv())


def load_wisdoms() -> List[str]:
    """
    This loads the wisdoms to search for.
    :return:
    """
    with open(WISDOMS_TXT, "r") as fh:
        return [
            wisdom for wisdom in fh
        ]


def load_wisdom2def_raw() -> pd.DataFrame:
    return pd.read_csv(WISDOM2DEF_RAW_TSV, sep="\t")


def load_wisdom2eg_raw() -> pd.DataFrame:
    return pd.read_csv(WISDOM2EG_RAW_TSV, sep="\t")


def load_wisdom2def() -> pd.DataFrame:
    """
    loads wisdom2def.tsv as a pandas
    :return:
    """
    return pd.read_csv(WISDOM2DEF_TSV, sep="\t")


def load_wisdom2eg() -> pd.DataFrame:
    """
    loads wisdom2eg.tsv -> you might need this?
    :return:
    """
    return pd.read_csv(WISDOM2EG_TSV, sep="\t")
