"""
e.g. 일반상식, 도서자료 기계 독해, 기계 독해.
"""
import json
from typing import Generator, Optional
from elasticsearch_dsl import Document
from storyteller.docs import GKDoc, SCDoc, MRDoc
from storyteller.paths import GK_DIR, SC_DIR, MR_DIR
import os


class Reader:

    def __iter__(self) -> Generator[Document, None, None]:
        """
        :param: depends on the corpus.
        :return: A list of documents - defined by storyteller/docs.py
        """
        raise NotImplementedError

    @staticmethod
    def build_doc(*args, **kwargs) -> Document:
        """
        This must match with the indices.
        :return:
        """
        raise NotImplementedError


class GKReader(Reader):
    """
    일반상식 데이터 리더.
    """
    def __iter__(self) -> Generator[GKDoc, None, None]:
        """
        :return: a list of samples
        """
        corpus_json_path = os.path.join(GK_DIR, "ko_wiki_v1_squad.json")
        with open(corpus_json_path, 'r') as fh:
            # refer to: storyteller/explore/explore_gk.py
            data = json.loads(fh.read())['data']
        for sample in data:
            for paragraph in sample['paragraphs']:
                yield self.build_doc(sents=paragraph['context'])

    @staticmethod
    def build_doc(**kwargs) -> GKDoc:
        return GKDoc(**kwargs)


class SCReader(Reader):
    """
    감성 대화 리더
    """

    def __iter__(self) -> Generator[SCDoc, None, None]:
        """
        :return:
        """
        train_json_path = os.path.join(SC_DIR, "Training", "감성대화말뭉치(최종데이터)_Training.json")
        val_json_path = os.path.join(SC_DIR, "Validation", "감성대화말뭉치(최종데이터)_Validation.json")

        with open(train_json_path, 'r') as fh_t, \
                open(val_json_path, 'r') as fh_v:
            train_json = json.loads(fh_t.read())
            val_json = json.loads(fh_v.read())
        # yield the train set, and then the validation set
        for sample in train_json:
            yield self.build_doc(sents=" ".join(sample['talk']['content'].values()),
                                 profile_id=sample['talk']['id']['profile-id'],
                                 talk_id=sample['talk']['id']['talk-id'])
        for sample in val_json:
            yield self.build_doc(sents=" ".join(sample['talk']['content'].values()),
                                 profile_id=sample['talk']['id']['profile-id'],
                                 talk_id=sample['talk']['id']['talk-id'])

    @staticmethod
    def build_doc(**kwargs) -> SCDoc:
        return SCDoc(**kwargs)


class MRReader(Reader):

    def __iter__(self) -> Generator[MRDoc, None, None]:
        normal_json_path = os.path.join(MR_DIR, "기계독해분야", "ko_nia_normal_squad_all.json")
        no_answer_json_path = os.path.join(MR_DIR, "기계독해분야", "ko_nia_noanswer_squad_all.json")
        clue_json_path = os.path.join(MR_DIR, "기계독해분야", "ko_nia_clue0529_squad_all.json")

        with open(normal_json_path, 'r') as fh_normal, \
                open(no_answer_json_path, 'r') as fh_no, \
                open(clue_json_path, 'r') as fh_clue:
            normal_json = json.loads(fh_normal.read())
            no_json = json.loads(fh_no.read())
            clue_json = json.loads(fh_clue.read())

        for sample in normal_json['data']:
            yield self.build_doc(sents=sample['paragraphs'][0]['context'],
                                 title=sample['title'])
        for sample in no_json['data']:
            yield self.build_doc(sents=sample['paragraphs'][0]['context'],
                                 title=sample['title'])
        for sample in clue_json['data']:
            yield self.build_doc(sents=sample['paragraphs'][0]['context'],
                                 title=sample['title'])

    def build_doc(*args, **kwargs) -> MRDoc:
        return MRDoc(**kwargs)


class DSReader(Reader):
    """
    문서 요약 데이터 리더
    """
    def __iter__(self, *args, **kwargs) -> Generator[dict, None, None]:
        pass

    @staticmethod
    def build_doc(**kwargs) -> Document:
        pass
