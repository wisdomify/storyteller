import os
import json
from storyteller.paths import MR_DIR, DS_DIR, SFC_DIR, KESS_DIR


def main():
    json_path = os.path.join(KESS_DIR, "kess.json")

    file = json.load(open(json_path, 'r', encoding='utf-8-sig'))

    data = file[0]['data'][0]


"""
{'data_set': '사회과학',
 'domain': '예술',
 'en': 'At the next bar, a sign of a gradually slowing agogic change appears, '
       'increasing relaxation and stability.',
 'file_name': '2017/숨겨진 V-I진행 브람스와 레거의 클라리넷 5중주에서 표현된 역동성',
 'ko': '다음 마디에서, 점점 느려지는 아고긱 변화 표시가 나와서, 이완과 안정감이 증가한다.',
 'license': 'open',
 'mt': 'At the next node, a sign of a gradually slowing agogic change appears, '
       'increasing relaxation and stability.',
 'sn': 'SCS54A1263',
 'source': '한국학술정보',
 'source_language': 'ko',
 'style': '문어체',
 'subdomain': '음악',
 'target_language': 'en'}

"""


if __name__ == '__main__':
    main()
