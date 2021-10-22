"""
exploring the structure of GK Corpus.
"""
from typing import List
from storyteller.paths import GK_DIR
from os import path
import json


def main():
    json_path = path.join(GK_DIR, "ko_wiki_v1_squad.json")
    with open(json_path, 'r') as fh:
        gk_json = json.loads(fh.read())

    data: List[dict] = gk_json['data']
    context = data[0]['paragraphs'][0]['context']
    print(context)  # this is what I want.


if __name__ == '__main__':
    main()
