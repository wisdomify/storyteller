import os
import re

import pandas as pd
from hanspell import spell_checker

from storyteller.paths import DATA_DIR
from storyteller.preprocess import parse, normalise


def explore_preprocess_parse():
    raw_df = pd.read_csv(os.path.join(DATA_DIR, 'tmp.tsv'), sep='\t')
    parsed_df = parse(raw_df)

    print(parsed_df)


def explore_preprocess_normalise():
    raw_df = pd.read_csv(os.path.join(DATA_DIR, 'tmp.tsv'), sep='\t')
    parsed_df = parse(raw_df)
    normalised_df = normalise(parsed_df)

    print(normalised_df)


def explore_convert_em_to_wisdom():
    wisdom = '가는 날이 장날'
    highlighted_sent = '비와 ㅇㅅㅇ #@시스템#사진# 엥? 비와? 헐 소나기는 여기가 아니고 거기였구나 소나기인듯 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ <em>가</em><em>는</em><em>날</em><em>이</em> <em>장날</em>이네 완전 여긴 여전히 해가 부글부글 끓고있음'
    t = re.sub(r"<em>.*</em>", "[WISDOM]", highlighted_sent)
    print(t)


def explore_spell_check():
    result = spell_checker.check(u'안녕 하세요. 저는 한국인 입니다. 이문장은 한글로 작성됬습니다.')

    print(result)


if __name__ == '__main__':
    # explore_convert_em_to_wisdom()
    # explore_preprocess_parse()
    explore_preprocess_normalise()
    # explore_spell_check()

