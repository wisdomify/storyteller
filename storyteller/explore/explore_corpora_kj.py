import os
import json
from storyteller.paths import MR_DIR, DS_DIR, SFC_DIR, KESS_DIR, KJ_DIR


def main():
    json_path = os.path.join(KJ_DIR, "kj.json")

    file = json.load(open(json_path, 'r', encoding='utf-8-sig'))

    data = file[0][0]

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
