"""
These builders are for building the tsv files, the dataset - the end product of storyteller.
This is where we split, augment, filter, pre-process data.
"""
import os
import smtpd

import pandas as pd
import requests
from typing import Callable, Tuple
from elasticsearch import Elasticsearch

from storyteller.elastic.searcher import Searcher
from storyteller.loaders import load_wisdom2def, load_wisdom2eg, load_wisdom2def_raw, load_wisdom2eg_raw, load_wisdoms
from storyteller.paths import (
    WISDOMIFY_TEST_TSV,
    WISDOM2DEF_RAW_TSV,
    WISDOM2DEF_TSV,
    WISDOM2DEF_TRAIN_TSV,
    WISDOM2DEF_VAL_TSV,
    WISDOM2EG_TSV,
    WISDOM2EG_TRAIN_TSV,
    WISDOM2EG_VAL_TSV,
    WISDOMS_TXT
)
from sklearn.model_selection import train_test_split


class Builder:

    def __call__(self, *args, **kwargs):
        # just build everything.
        # build wisdoms.txt
        # build wisdomify_test.tsv
        # build wisdom2def package.
        # build wisdom2eg package.
        raise NotImplementedError

    @staticmethod
    def build_from_url(url: str, local_path: str):
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        with open(local_path, 'w') as fh:
            fh.write(r.text)


class WisdomifyTestBuilder(Builder):
    """
    builds (downloads) wisdomify_test.tsv from Google Sheets
    """
    def __call__(self, *args, **kwargs):
        self.build_from_url(url=os.getenv("WISDOMIFY_TEST_URL"),
                            local_path=WISDOMIFY_TEST_TSV)


class WisdomsBuilder(Builder):
    """
    builds (downloads) wisdomify_test.tsv from Google Sheets
    """
    def __call__(self, *args, **kwargs):
        self.build_from_url(url=os.getenv("WISDOMS_URL"),
                            local_path=WISDOMS_TXT)


class Wisdom2SentBuilder(Builder):

    def __init__(self, train_ratio: float, seed: int):
        self.train_ratio = train_ratio
        self.seed = seed

    def __call__(self, *args, **kwargs):
        # --- these three steps are all you need to implement.
        self.build_wisdom2sent_raw()  # build wisdom2sent_raw.tsv
        self.build_wisdom2sent()  # build wisdom2sent.tsv
        self.build_train_val()  # build wisdom2sent_train.tsv &  wisdom2sent_val.tsv

    # --- to be implemented --- #
    def build_wisdom2sent_raw(self):
        raise NotImplementedError

    def build_wisdom2sent(self):
        raise NotImplementedError

    @staticmethod
    def load_wisdom2sent() -> pd.DataFrame:
        raise NotImplementedError

    @staticmethod
    def train_val_paths() -> Tuple[str, str]:
        raise NotImplementedError

    def build_train_val(self):
        """
        Split into train & validation set, and save them.
        :return:
        """
        all_df = self.load_wisdom2sent()
        total = len(all_df)
        tran_size = int(total * self.train_ratio)
        val_size = total - tran_size
        train_df, val_df = train_test_split(all_df, train_size=tran_size,
                                            test_size=val_size, random_state=self.seed,
                                            shuffle=True)
        train_path, val_path = self.train_val_paths()
        train_df.to_csv(train_path, sep="\t", index=False)
        val_df.to_csv(val_path, sep="\t", index=False)


class Wisdom2DefBuilder(Wisdom2SentBuilder):
    """
    1. first, builds (downloads) wisdom2def_raw.tsv from Google Sheets
    2. process wisdom2def_raw.tsv to build wisdom2def.tsv (involves augmentation)
    3. split wisdom2def.tsv into wisdom2def_train.tsv * wisdom2def_val.tsv
    """

    def build_wisdom2sent_raw(self):
        """
        Just download wisdom2sent_raw.tsv from Google Sheets
        :return:
        """
        self.build_from_url(url=os.getenv("WISDOM2DEF_RAW_URL"),
                            local_path=WISDOM2DEF_RAW_TSV)

    def build_wisdom2sent(self):
        """
        Augment wisdom2sent_raw.tsv to build wisdom2sent.tsv
        :return:
        """
        wisdom2def_raw_df = load_wisdom2def_raw()
        # just write it as-is as of right now.
        wisdom2def_raw_df.to_csv(WISDOM2DEF_TSV, sep="\t")

    @staticmethod
    def load_wisdom2sent() -> pd.DataFrame:
        return load_wisdom2def()

    @staticmethod
    def train_val_paths() -> Tuple[str, str]:
        return WISDOM2DEF_TRAIN_TSV, WISDOM2DEF_VAL_TSV


class Wisdom2EgBuilder(Wisdom2SentBuilder):
    """
    # 1. first, builds (searches) wisdom2eg_raw.tsv from ES
    # 2. process wisdom2eg_raw.tsv to build wisdom2eg.tsv
    # 3. split wisdom2eg.tsv into wisdom2eg_train.tsv * wisdom2eg_val.tsv
    """

    def __init__(self, searcher: Searcher, train_ratio: float, seed: int):
        super().__init__(train_ratio, seed)
        self.searcher = searcher
        self.train_ratio = train_ratio
        self.seed = seed

    def build_wisdom2sent_raw(self):
        """
        This involves searching the wisdoms on ES indices.
        :return:
        """
        # TODO - implement this later
        pass

    def build_wisdom2sent(self):
        """
        This may involve some parsing. (e.g. <idiom>산 넘어 산</idiom>이라고 -> [WISDOM]이라고
        :return:
        """
        # TODO - implement this later
        pass

    @staticmethod
    def load_wisdom2sent() -> pd.DataFrame:
        return load_wisdom2eg()

    @staticmethod
    def train_val_paths() -> Tuple[str, str]:
        return WISDOM2EG_TRAIN_TSV, WISDOM2EG_VAL_TSV
