import json
import re

import pandas as pd

from typing import Tuple
from sklearn.model_selection import train_test_split
from soynlp.normalizer import emoticon_normalize, only_text
from hanspell import spell_checker


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
    # TODO: normalise spacing (soyspacing)
    # TODO: normalise grammar errors (py-hanspell)

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
    # py-hanspell을 설치해야하는 데 pip으로 설치하면 이전 버전의 pip으로 실행되서 에러가 발생한다.
    # 반드시 해당 프로젝트의 리포를 클론후 storyteller 프로젝트 환경이 활성화되어 있는 상태에서 `python3 setup.py install`을 실행해야한다.
    # 이 스텝이 가장 time consuming 한데 흠...
    df['eg'] = df['eg'].apply(lambda r: spell_checker.check(r).checked)  # grammar check

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
