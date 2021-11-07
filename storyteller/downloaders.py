import pandas as pd
import io
import requests
import json
from tqdm import tqdm
from storyteller.elastic.crud import Searcher
from storyteller.elastic.docs import Story
from storyteller.urls import WISDOM2DEF_RAW_V0, WISDOM2TEST_V0, WISDOMS_V1, WISDOMS_V0, WISDOM2DEF_RAW_V1


def dl_from_url(url: str) -> str:
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = 'utf-8'
    return r.text


def dl_wisdoms(ver: str) -> pd.DataFrame:
    if ver == "v0":
        text = dl_from_url(WISDOMS_V0)
    elif ver == "v1":
        text = dl_from_url(WISDOMS_V1)
    else:
        raise ValueError
    return pd.read_csv(io.StringIO(text), delimiter="\t")


def dl_wisdom2query_raw(ver: str) -> pd.DataFrame:
    if ver == "v0":
        text = dl_from_url(WISDOM2TEST_V0)
    else:
        raise ValueError
    return pd.read_csv(io.StringIO(text), delimiter="\t")


def dl_wisdom2def_raw(ver: str) -> pd.DataFrame:
    if ver == "v0":
        text = dl_from_url(WISDOM2DEF_RAW_V0)
    elif ver == "v1":
        text = dl_from_url(WISDOM2DEF_RAW_V1)
    else:
        raise ValueError
    return pd.read_csv(io.StringIO(text), delimiter="\t")


def dl_wisdom2eg_raw(ver: str, searcher: Searcher) -> pd.DataFrame:
    wisdoms_df = dl_wisdoms(ver)
    total = len(wisdoms_df)
    rows = list()
    for _, row in tqdm(wisdoms_df.iterrows(), desc="searching for wisdoms on stories...", total=total):
        wisdom = row['wisdom']
        raw = searcher(wisdom, ",".join(Story.all_indices()), size=10000)
        # https://stackoverflow.com/a/18337754
        raw = json.dumps(raw, ensure_ascii=False)
        rows.append((wisdom, raw))

    return pd.DataFrame(data=rows, columns=["wisdom", "eg"])
