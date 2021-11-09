import os
import json
from storyteller.paths import MR_DIR, DS_DIR, SFC_DIR, KESS_DIR, KJ_DIR, KCSS_DIR, SFKE_DIR, KSNS_DIR, KC_DIR, KETS_DIR


def main():
    json_path = os.path.join(KETS_DIR, 'kets.json')

    file = json.load(open(json_path, 'r', encoding='utf-8-sig'))

    data = file[0]['data'][0]


"""
{'sn': 'TNS01N2228',
 'file_name': '특허_6주_1020120031826',
 'data_set': '기술과학',
 'domain': '기계',
 'subdomain': '의공학',
 'source': '특허정보원',
 'ko': '촬영장치(11) 및 에너지 발생장치(12)는 로봇(10)의 말단부(40)의 측면에 마련된다.',
 'mt': 'The photographing device 11 and the energy generating device 12 are provided on the side of the distal end 40 of the robot 10.',
 'en': 'The photographing device 11 and the energy generating device 12 are provided on the side of the distal end part 40 of the robot 10.',
 'source_language': 'ko',
 'target_language': 'en',
 'license': 'open',
 'style': '문어체'}
"""

if __name__ == '__main__':
    main()
