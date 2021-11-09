"""
exploring the structure of cvc Corpus.
"""
import os
from pprint import pprint
from typing import List, Optional
from storyteller.paths import BS_DIR, CVC_DIR
from os import path
import json


def explore_cvc():
    train_1 = json.load(open(os.path.join(CVC_DIR, "train_1.json"), encoding='utf-8-sig'))
    train_2 = json.load(open(os.path.join(CVC_DIR, "train_2.json"), encoding='utf-8-sig'))
    train_3 = json.load(open(os.path.join(CVC_DIR, "train_3.json"), encoding='utf-8-sig'))

    val_1 = json.load(open(os.path.join(CVC_DIR, "val_1.json"), encoding='utf-8-sig'))
    val_2 = json.load(open(os.path.join(CVC_DIR, "val_2.json"), encoding='utf-8-sig'))
    val_3 = json.load(open(os.path.join(CVC_DIR, "val_3.json"), encoding='utf-8-sig'))

    print(train_1)
    # meaningless data


if __name__ == '__main__':
    # get_files(BS_DIR)
    # merge_json_files(on=BS_DIR, to=os.path.join(BS_DIR, 'bs.json'))
    explore_cvc()
