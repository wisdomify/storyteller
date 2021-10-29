import os
import json
from storyteller.paths import MR_DIR, DS_DIR, SFC_DIR


def main():
    json_path = os.path.join(SFC_DIR, "sfc.json")

    file = json.load(open(json_path, 'r', encoding='utf-8-sig'))

    data = file[0]['data'][0]


"""
{'attr': '초록',
 'date': '2019.01.31',
 'doc_id': '1020120090791',
 'doc_type': '특허',
 'ipc': 'G06K 7/00(2006.01.01) H01R 13/639(2006.01.01) H01R 13/50(2006.01.01) '
        'H01R 12/71(2011.01.01) H04B 1/3816(2014.01.01)',
 'reg_no': '1019463240000',
 'sentence': [{'NE': [{'begin': 6,
                       'end': 10,
                       'entity': '전자 장치',
                       'id': 0,
                       'type': 'TM'},
                      {'begin': 18,
                       'end': 25,
                       'entity': '카드 소켓 장치',
                       'id': 1,
                       'type': 'TM'},
                      {'begin': 50,
                       'end': 55,
                       'entity': '소켓 하우징',
                       'id': 2,
                       'type': 'TM'},
                      {'begin': 62,
                       'end': 67,
                       'entity': '소켓 하우징',
                       'id': 3,
                       'type': 'TM'},
                      {'begin': 70,
                       'end': 71,
                       'entity': '상부',
                       'id': 4,
                       'type': 'TM'},
                      {'begin': 106,
                       'end': 110,
                       'entity': '소켓 커버',
                       'id': 5,
                       'type': 'TM'},
                      {'begin': 116,
                       'end': 121,
                       'entity': '소켓 하우징',
                       'id': 6,
                       'type': 'TM'},
                      {'begin': 143,
                       'end': 148,
                       'entity': '소켓 하우징',
                       'id': 7,
                       'type': 'TM'},
                      {'begin': 159,
                       'end': 160,
                       'entity': '단부',
                       'id': 8,
                       'type': 'TM'},
                      {'begin': 168,
                       'end': 173,
                       'entity': '소켓 스토퍼',
                       'id': 9,
                       'type': 'TM'},
                      {'begin': 185,
                       'end': 190,
                       'entity': '소켓 스토퍼',
                       'id': 10,
                       'type': 'TM'},
                      {'begin': 206,
                       'end': 211,
                       'entity': '소켓 하우징',
                       'id': 11,
                       'type': 'TM'},
                      {'begin': 258,
                       'end': 262,
                       'entity': '전자 장치',
                       'id': 12,
                       'type': 'TM'}],
               'text': '본 발명은 전자 장치에 설치되는 카드 소켓 장치에 관한 것으로서, 카드 수용 공간을 갖는 소켓 '
                       '하우징과, 상기 소켓 하우징의 상부에 설치되어 상기 카드 수용 공간에 장착되는 카드를 탄지하는 '
                       '소켓 커버및 상기 소켓 하우징에 회동 가능하게 힌지 결합되어 상기 소켓 하우징에 장착된 카드의 '
                       '단부를 지지하는 소켓 스토퍼를 포함하여, 상기 소켓 스토퍼에 의해 상기 카드가 상기 소켓 '
                       '하우징에서 임의로 탈거되는 것을 방지하여, 기기의 오동작을 미연에 방지하고, 결과적으로 전자 '
                       '장치의 신뢰성을 향상시킬 수 있다.'}],
 'sentno': 1,
 'title': '카드 소켓 장치'}
"""


if __name__ == '__main__':
    main()
