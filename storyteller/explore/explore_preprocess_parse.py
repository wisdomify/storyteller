import os

import pandas as pd

from storyteller.paths import DATA_DIR
from storyteller.preprocess import parse


def explore_preprocess_parse():
    raw_df = pd.read_csv(os.path.join(DATA_DIR, 'tmp.tsv'), sep='\t')
    parsed_df = parse(raw_df)

    print(parsed_df)


if __name__ == '__main__':
    explore_preprocess_parse()
