import os
import json
from storyteller.paths import MR_DIR, DS_DIR, SFC_DIR, KESS_DIR, KJ_DIR, KCSS_DIR, SFKE_DIR


def main():
    json_path = os.path.join(SFKE_DIR, "sfke.json")

    file = json.load(open(json_path, 'r', encoding='utf-8-sig'))

    data = file[0][0]

"""
{'sid': 1,
 '분야': '가정통신문',
 '한국어': '본교에서는 학생들의 소질 계발과 실력 향상은 물론 학부모님의 사교육비 경감을 위하여 방과후학교를 내실 있게 운영하고자 노력하고 있습니다.',
 '영어': "In order to improve students' talents and skills, this school strives to operate after-school programs in a substantial manner to reduce parents' private education expenses.",
 '한국어_어절수': 17,
 '영어_단어수': 25,
 '길이_분류': 3,
 '난이도': '중',
 '수행기관': '플리토'}
"""


if __name__ == '__main__':
    main()
