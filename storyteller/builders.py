"""
These builders are for building the tsv files, the dataset - the end product of storyteller.
This is where we split, augment, filter, pre-process data.
"""
import os
from typing import Optional

import pandas as pd
import requests
from elasticsearch import Elasticsearch
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

    def __init__(self, seed: int, train_portion: float):
        self.seed = seed
        self.train_portion = train_portion
        self.wisdom2sent_path: Optional[str] = None
        self.wisdom2sent_train_path: Optional[str] = None
        self.wisdom2sent_val_path: Optional[str] = None

    def __call__(self, *args, **kwargs):
        self.build_wisdom2sent_raw()  # build wisdom2sent_raw.tsv
        self.build_wisdom2sent()  # build wisdom2sent.tsv
        self.init_paths()
        self.build_train_val()

    def build_wisdom2sent_raw(self):
        raise NotImplementedError

    def build_wisdom2sent(self):
        raise NotImplementedError

    def init_paths(self):
        raise NotImplementedError

    def build_train_val(self):
        all_df = pd.read_csv(self.wisdom2sent_path, sep="\t")
        total = all_df.count
        tran_size = int(total * self.train_portion)
        val_size = total - tran_size
        train_df, val_df = train_test_split(all_df, train_size=tran_size,
                                            test_size=val_size, random_state=self.seed,
                                            shuffle=True)
        train_df.to_csv(self.wisdom2sent_train_path, sep="\t", index=False)
        val_df.to_csv(self.wisdom2sent_val_path, sep="\t", index=False)


class Wisdom2DefBuilder(Wisdom2SentBuilder):
    """
    1. first, builds (downloads) wisdom2def_raw.tsv from Google Sheets
    2. process wisdom2def_raw.tsv to build wisdom2def.tsv (involves augmentation)
    3. split wisdom2def.tsv into wisdom2def_train.tsv * wisdom2def_val.tsv
    """

    def init_paths(self):
        self.wisdom2sent_path = WISDOM2DEF_TSV
        self.wisdom2sent_train_path = WISDOM2DEF_TRAIN_TSV
        self.wisdom2sent_val_path = WISDOM2DEF_VAL_TSV

    def build_wisdom2sent_raw(self):
        """
        this involve downloading it from Google Sheets
        :return:
        """
        self.build_from_url(url=os.getenv("WISDOM2DEF_RAW_URL"),
                            local_path=WISDOM2DEF_RAW_TSV)

    def build_wisdom2sent(self):
        """
        This may involve some augmentation
        :return:
        """
        pass


class Wisdom2EgBuilder(Wisdom2SentBuilder):

    def __init__(self, client: Elasticsearch, seed: int, train_portion: float):
        super().__init__(seed, train_portion)
        self.client = client

    def init_paths(self):
        self.wisdom2sent_path = WISDOM2EG_TSV
        self.wisdom2sent_train_path = WISDOM2EG_TRAIN_TSV
        self.wisdom2sent_val_path = WISDOM2EG_VAL_TSV

    def build_wisdom2sent_raw(self):
        """
        This involves searching the wisdoms on ES indices.
        :return:
        """
        pass

    def build_wisdom2sent(self):
        """
        This may involve some parsing. (e.g. <idiom>산 넘어 산</idiom>이라고 -> [WISDOM]이라고
        :return:
        """
        pass
