import json
import re

import pandas as pd

from typing import Tuple
from sklearn.model_selection import train_test_split
from soynlp.normalizer import emoticon_normalize, only_text

from storyteller.utils.grammar_checker import check_grammar


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

    # =============== normalise emoticons and shorts =============== #
    df['eg'] = df['eg'].apply(lambda r: re.sub('\.*!+', '!', r))  # (....)! match
    df['eg'] = df['eg'].apply(lambda r: re.sub('\.*\?+', '?', r))  # (....)? match
    df['eg'] = df['eg'].apply(lambda r: re.sub('\.+', '.', r))  # (....). match
    df['eg'] = df['eg'].apply(lambda r: re.sub(',+', ',', r))  # (,,,,), match
    # ㄱ-ㅎ이 따로 쓰일 경우를 대비해 ㄱ-ㅎ을 매칭시키게했었으나
    # ㅋ가 3번 사용한경우는 emoticon_normalise 에 걸리지 않아 자음 단독으로 쓰인 경우도 제거
    df['eg'] = df['eg'].apply(lambda r: re.sub('[^A-Za-z0-9가-힣\s\[\].,!?\"\']', '', r))

    df['eg'] = df['eg'].apply(lambda r: emoticon_normalize(only_text(r), num_repeats=1))

    # ===================== normalise spacing ===================== #
    df['eg'] = df['eg'].apply(lambda r: re.sub('\s+', ' ', r))  # multiple spacing match

    # ==================== grammar error check +=================== #

    df['eg'] = df['eg'].apply(lambda r: check_grammar(r))  # grammar check

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
