import json
import re

import pandas as pd

from typing import Tuple
from sklearn.utils import resample
from sklearn.model_selection import train_test_split


def augment(df: pd.DataFrame) -> pd.DataFrame:
    # TODO implement augmentation.
    return df


def parse(df: pd.DataFrame) -> pd.DataFrame:
    """
    parse <em> ...</em>  to [WISDOM].
    :param df: raw_df includes 'wisdom' and 'eg' field
    :return: 'eg' field parsed df
    """

    df['eg'] = df['eg'].apply(
        # return list of example only on 'eg' column (proverb is converted to [WISDOM])
        lambda r: list(map(
            # while iterating list of 'hits'
            # convert <em> ... lalib ... </em> to [WISDOM]
            lambda hit: re.sub(r"<em>.*</em>", "[WISDOM]", hit['highlight']['sents'][0]),
            # loading json to dict -> taking dict['hits']['hits']
            json.loads(r)['hits']['hits']
        ))
    )

    # 'eg' column contains list object
    # -> converted to single value with multiple columns
    df = df.explode('eg')

    return df


def normalise(df: pd.DataFrame) -> pd.DataFrame:
    """
    1. normalise the emoticons.
    2. normalise the spacings.
    3. normalise grammatical errors.
    :param df:
    :return:
    """
    # TODO: implement normalisation
    return df


def upsample(df: pd.DataFrame, seed: int) -> pd.DataFrame:
    counts = df.groupby(by='wisdom').count().sort_values(by='eg', ascending=False)['eg']
    major_count = counts.values[0]
    major_wisdom = counts.index[0]

    # Upsample minority class
    total_df = df.loc[df['wisdom'] == major_wisdom]
    for wis, ct in counts[1:].items():
        df_minority_upsampled = resample(df[df['wisdom'] == wis],
                                         replace=True,  # sample with replacement
                                         n_samples=major_count,  # to match majority class
                                         random_state=seed)  # reproducible results

        total_df = total_df.append(df_minority_upsampled)

    return total_df


def split_train_val(df: pd.DataFrame, train_ratio: float, seed: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    total = len(df)
    train_size = int(total * train_ratio)
    val_size = total - train_size
    train_df, val_df = train_test_split(df, train_size=train_size,
                                        test_size=val_size, random_state=seed,
                                        shuffle=True)
    return train_df, val_df
