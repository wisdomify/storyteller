import os
import json
from storyteller.paths import MR_DIR


def main():
    normal_json_path = os.path.join(MR_DIR, "기계독해분야", "ko_nia_normal_squad_all.json")
    no_answer_json_path = os.path.join(MR_DIR, "기계독해분야", "ko_nia_noanswer_squad_all.json")
    clue_json_path = os.path.join(MR_DIR, "기계독해분야", "ko_nia_clue0529_squad_all.json")

    with open(normal_json_path, 'r') as fh_normal,\
         open(no_answer_json_path, 'r') as fh_no,\
         open(clue_json_path, 'r') as fh_clue:
        normal_json = json.loads(fh_normal.read())
        no_json = json.loads(fh_no.read())
        clue_json = json.loads(fh_clue.read())

    for sample in normal_json['data']:
        title = sample['title']
        # all of them are 1, hence, the title is unique to each paragraph.
        assert len(sample['paragraphs']) == 1

    for sample in no_json['data']:
        title = sample['title']
        # all of them are 1, hence, the title is unique to each paragraph.
        assert len(sample['paragraphs']) == 1

    for sample in clue_json['data']:
        title = sample['title']
        # all of them are 1, hence, the title is unique to each paragraph.
        assert len(sample['paragraphs']) == 1

# all of them are 1 - nice.


if __name__ == '__main__':
    main()
