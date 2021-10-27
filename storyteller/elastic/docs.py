"""
for defining Elasticsearch docs and the indices.
"""
import os
import json
from collections import Generator
from elasticsearch_dsl import Document, Text, Keyword
from storyteller.paths import GK_DIR, SC_DIR, MR_DIR


class Story(Document):
    # --- common fields --- #
    sents = Text(analyzer="nori_analyzer")

    @staticmethod
    def stream_from_corpus() -> Generator['Story', None, None]:
        """
        :return: a stream of Stories.
        """
        raise NotImplementedError

    @staticmethod
    def settings() -> dict:
        """
        returns the settings for all the indices,
        that are consistent throughout whatever korean indices we make.
        https://prohannah.tistory.com/73
        https://coding-start.tistory.com/167
        :return:
        """
        return {
            "analysis": {
                "tokenizer": {
                    "nori_tokenizer": {
                        "type": "nori_tokenizer",
                        # 마곡역 -> 마곡역, 마곡, 역
                        "decompound_mode": "mixed",
                    }
                },
                "analyzer": {
                    "nori_analyzer": {
                        "tokenizer": "nori_tokenizer",
                        "filter": [
                            "nori_filter"
                        ]
                    }
                },
                "filter": {
                    "nori_filter": {
                        "type": "nori_part_of_speech",
                        # 공백외에 전부 허용 - 이걸.. 어떻게 하지..
                        "stoptags": []
                    }
                }
            }
        }


class GK(Story):
    """
    일반 상식 인덱스
    """
    @staticmethod
    def stream_from_corpus() -> Generator['GK', None, None]:
        corpus_json_path = os.path.join(GK_DIR, "ko_wiki_v1_squad.json")
        with open(corpus_json_path, 'r') as fh:
            # refer to: storyteller/explore/explore_gk.py
            data = json.loads(fh.read())['data']
        for sample in data:
            for paragraph in sample['paragraphs']:
                yield GK(sents=paragraph['context'])

    class Index:
        name = "gk_story"
        settings = Story.settings()


class SC(Story):
    """
    감성 대화 인덱스
    """
    # --- additional fields for SC --- #
    profile_id = Keyword()
    talk_id = Keyword()

    @staticmethod
    def stream_from_corpus() -> Generator['SC', None, None]:
        train_json_path = os.path.join(SC_DIR, "Training", "감성대화말뭉치(최종데이터)_Training.json")
        val_json_path = os.path.join(SC_DIR, "Validation", "감성대화말뭉치(최종데이터)_Validation.json")

        for json_path in (train_json_path, val_json_path):
            with open(json_path, 'r') as fh:
                corpus_json = json.loads(fh.read())
                for sample in corpus_json:
                    yield SC(sents=" ".join(sample['talk']['content'].values()),
                             profile_id=sample['talk']['id']['profile-id'],
                             talk_id=sample['talk']['id']['talk-id'])

    class Index:
        name = "sc_story"
        settings = Story.settings()


class MR(Story):
    """
    기계 독해 인덱스
    """
    # --- additional fields for MR --- #
    title = Keyword()

    @staticmethod
    def stream_from_corpus() -> Generator['MR', None, None]:
        normal_json_path = os.path.join(MR_DIR, "기계독해분야", "ko_nia_normal_squad_all.json")
        no_answer_json_path = os.path.join(MR_DIR, "기계독해분야", "ko_nia_noanswer_squad_all.json")
        clue_json_path = os.path.join(MR_DIR, "기계독해분야", "ko_nia_clue0529_squad_all.json")

        for json_path in (normal_json_path, no_answer_json_path, clue_json_path):
            with open(normal_json_path, 'r') as fh:
                corpus_json = json.loads(fh.read())
                for sample in corpus_json['data']:
                    yield MR(sents=sample['paragraphs'][0]['context'],
                             title=sample['title'])

    class Index:
        name = "mr_story"
        settings = Story.settings()

