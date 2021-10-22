import json
from storyteller.paths import SC_DIR
from os import path


def main():
    train_json_path = path.join(SC_DIR, "Training", "감성대화말뭉치(최종데이터)_Training.json")

    with open(train_json_path, 'r') as fh:
        train_json = json.loads(fh.read())

    # just space-join all the contents into sents
    sents = " ".join(train_json[0]['talk']['content'].values())
    print(sents)
    print(train_json[0]['talk']['id'])



if __name__ == '__main__':
    main()
