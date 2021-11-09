import os
import json
from storyteller.paths import MR_DIR, DS_DIR, SFC_DIR, KESS_DIR, KJ_DIR, KCSS_DIR, SFKE_DIR, KSNS_DIR, KC_DIR, KETS_DIR, \
    KEPT_DIR


def main():
    json_path = os.path.join(KEPT_DIR, 'kept.json')

    file = json.load(open(json_path, 'r', encoding='utf-8-sig'))

    data = file[0][0]


"""
{'ID': 20261311,
 '날짜': 20190306,
 '자동분류1': '문화,학술_문화재',
 '자동분류2': '문화,방송_연예',
 '자동분류3': '문화,출판',
 'URL': 'http://news.kmib.co.kr/article/view.asp?arcid=0924065317&code=23111515',
 '언론사': '국민일보',
 '원문': '그녀가 할 수 있는 것은 우는 것이었습니다.',
 '번역문': 'All she could do was cry.'}
"""

if __name__ == '__main__':
    main()
