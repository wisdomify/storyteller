import os
import json

import pandas as pd

from storyteller.paths import KOREA_UNIV_DIR


def main():
    csv_files = list()
    for root, sub_dirs, files in os.walk(KOREA_UNIV_DIR):
        if files:
            csv_files += list(map(lambda f: os.path.join(root, f), files))

    for csv_file in csv_files:
        if csv_file.split('.')[-1] == 'tsv':
            df = pd.read_csv(csv_file, sep='\t')
        else:
            df = pd.read_csv(csv_file)

        if 'full' not in df.keys():
            print("#", csv_file)
        for index, row in df.iterrows():
            print(row['eg_id'], row['full'].replace('/n', ''))

"""
{'관리번호': 'KO-JA-2020-SOCI-000501',
 '분야': '사회/노동/복지',
 '한국어': '현대차는 지난달 27일 취업규칙 변경안을 고용노동부에 제출했다.',
 '일본어': 'ヒュンダイ自動車は先月27日、就業規則変更案を雇用労働部に提出した。',
 '한국어_어절수': 7,
 '일본어_글자수': 30,
 '길이_분류': 1,
 '출처': 'https://www.hankyung.com/economy/article/2019070896481',
 '수행기관': '플리토'}

"""


if __name__ == '__main__':
    main()
