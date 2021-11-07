import json
import re
from typing import Tuple
import pandas as pd
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
    return df.apply(get_highlighted_hits, axis=1)\
        .explode('eg')


def get_highlighted_hits(df: pd.DataFrame) -> pd.DataFrame:
    df['eg'] = list(map(
        lambda hit: convert_em_to_wisdom(hit['highlight']['sents'][0]),
        json.loads(df['eg'])['hits']['hits']
    ))
    return df


def convert_em_to_wisdom(highlight: str) -> str:
    return re.sub(r"<em>.*</em>", "[WISDOM]", highlight)


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


def upsample(df: pd.DataFrame) -> pd.DataFrame:
    # TODO: implement upsampling
    return df


def split_train_val(df: pd.DataFrame, train_ratio: float, seed: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    total = len(df)
    train_size = int(total * train_ratio)
    val_size = total - train_size
    train_df, val_df = train_test_split(df, train_size=train_size,
                                        test_size=val_size, random_state=seed,
                                        shuffle=True)
    return train_df, val_df
