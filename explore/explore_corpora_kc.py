import os
import json
from storyteller.paths import MR_DIR, DS_DIR, SFC_DIR, KESS_DIR, KJ_DIR, KCSS_DIR, SFKE_DIR, KSNS_DIR, KC_DIR


def main():
    json_path = os.path.join(KC_DIR, "kc.json")

    file = json.load(open(json_path, 'r', encoding='utf-8-sig'))

    data = file[0][0]

"""
{'SPEAKER': '고객',
 'SENTENCE': '애가 고등학교 1학년인데 태권도 하려면 수강료가 얼마쯤?',
 'DOMAINID': 'C',
 'DOMAIN': '학원',
 'CATEGORY': '태권도',
 'SPEAKERID': 1,
 'SENTENCEID': 1,
 'MAIN': '교육비문의',
 'SUB': nan,
 'QA': 'Q',
 'QACNCT': nan,
 'MQ': '애가 고등학교 1학년인데 태권도 하려면 수강료가 얼마쯤?',
 'SQ': nan,
 'UA': nan,
 'SA': nan,
 '개체명': '고등학교 1학년, 태권도, 수강료, 얼마',
 '용어사전': nan,
 '지식베이스': '고등학교 1학년/대상, 태권도/과목'}
"""

if __name__ == '__main__':
    main()
