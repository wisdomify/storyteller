import json
import os

from storyteller.paths import CVC_DIR, DS_DIR, SFC_DIR, KESS_DIR, KJ_DIR, KCSS_DIR


def get_files(on: str):
    jsons = list()
    for root, sub_dirs, files in os.walk(on):
        if files:
            jsons += list(map(lambda file: os.path.join(root, file), files))

    return jsons


def merge_json_files(on: str, to: str):
    result = list()
    files = get_files(on)
    for i, f1 in enumerate(files):
        print(i, end=' ')
        with open(f1, 'r', encoding='utf-8') as infile:
            try:
                jf = json.load(infile)
                result.append(jf)
            except:
                continue

    with open(to, 'w', encoding='UTF-8-sig') as output_file:
        json.dump(result, output_file, ensure_ascii=False)


if __name__ == '__main__':
    merge_json_files(on=os.path.join(KCSS_DIR),
                     to=os.path.join(KCSS_DIR, 'kcss.json'))
