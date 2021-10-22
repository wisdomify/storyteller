"""
e.g. 일반상식, 도서자료 기계 독해, 기계 독해.
"""
from typing import Generator
from storyteller.paths import GK_DIR, SC_DIR
from os import path
import json


class Reader:
    def __iter__(self) -> Generator[dict, None, None]:
        """
        the
        [
            {
              content: str
              meta: ...
            },
            {
              content: str
              meta: ...
            }
        ]
        :param: depends on the corpus.
        :return: A list of dicts (a list of samples)
        """
        raise NotImplementedError

    @staticmethod
    def build_sample(sents: str, meta: dict) -> dict:
        """
        :param sents: sentences merged into a string.
        :param meta: any meta data associated with sents. (e.g. corpus, id)
        :return:
        """
        return {
            'sents': sents,
            'meta': meta
        }


class GKReader(Reader):
    """
    일반상식 데이터 리더.
    """
    def __iter__(self) -> Generator[dict, None, None]:
        """
        :return: a list of samples
        """
        corpus_json_path = path.join(GK_DIR, "ko_wiki_v1_squad.json")
        with open(corpus_json_path, 'r') as fh:
            # refer to: storyteller/explore/explore_gk.py
            data = json.loads(fh.read())['data']
        for sample in data:
            for paragraph in sample['paragraphs']:
                yield self.build_sample(sents=paragraph['context'],
                                        meta={'corpus': 'gk'})


class SCReader(Reader):
    """
    감성 대화 리더
    """
    def __iter__(self) -> Generator[dict, None, None]:
        """
        :return:
        """
        train_json_path = path.join(SC_DIR, "Training", "감성대화말뭉치(최종데이터)_Training.json")
        val_json_path = path.join(SC_DIR, "Validation", "감성대화말뭉치(최종데이터)_Validation.json")

        with open(train_json_path, 'r') as fh_t, \
                open(val_json_path, 'r') as fh_v:
            train_json = json.loads(fh_t.read())
            val_json = json.loads(fh_v.read())
        # yield the train set, and then the validation set
        for sample in train_json:
            yield self.build_sample(sents=" ".join(sample['talk']['content'].values()),
                                    meta={'corpus': 'sc', 'ids': sample['talk']['id']})
        for sample in val_json:
            yield self.build_sample(sents=" ".join(sample['talk']['content'].values()),
                                    meta={'corpus': 'sc', 'ids': sample['talk']['id']})


class DSReader(Reader):
    """
    문서 요약 데이터 리더
    """

    def __iter__(self, *args, **kwargs) -> Generator[dict, None, None]:
        raise NotImplementedError
