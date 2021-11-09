import os
import json
from storyteller.paths import MR_DIR, DS_DIR, SFC_DIR, KESS_DIR, KJ_DIR, KCSS_DIR


def main():
    json_path = os.path.join(KCSS_DIR, "kcss.json")

    file = json.load(open(json_path, 'r', encoding='utf-8-sig'))

    data = file[0][0]

"""
{'관리번호': 'KO-ZH-2020-SOCI-000501',
 '분야': '사회/노동/복지',
 '한국어': '루즈벨트 행정부가 대공황으로 무너진 미국사회를 재건하기 위해 실행한 제반 정책이었다.',
 '중국어': '这是罗斯福政府为了重建因大萧条而崩溃的美国社会而实施的各项政策。',
 '한국어_어절수': 10,
 '중국어_글자수': 31,
 '길이_분류': 2,
 '출처': 'http://uci.or.kr/G703:RA101-01101101.20200529050533001:1',
 '수행기관': '플리토'}


"""


if __name__ == '__main__':
    main()
