"""
exploring the structure of BS Corpus.
"""
import os
from pprint import pprint
from typing import List, Optional
from storyteller.paths import BS_DIR
from os import path
import json


def explore_bs():
    json_path = path.join(BS_DIR, "bs.json")
    with open(json_path, 'r', encoding='UTF-8-sig') as fh:
        bs_json = json.loads(fh.read())

    data: List[dict] = bs_json
    sample = data[0]['passage']
    sample_id = data[0]['passage_id']
    print(sample)  # this is what I want.
    print(sample_id)


if __name__ == '__main__':
    # get_files(BS_DIR)
    # merge_json_files(on=BS_DIR, to=os.path.join(BS_DIR, 'bs.json'))
    explore_bs()
