"""
for defining Elasticsearch docs and the indices.
"""
import os
import json
from typing import Generator
from elasticsearch_dsl import Document, Text, Keyword
from storyteller.paths import GK_DIR, SC_DIR, MR_DIR, BS_DIR, DS_DIR, SFC_DIR, KESS_DIR, KJ_DIR, KCSS_DIR, SFKE_DIR, \
    KSNS_DIR, KC_DIR, KETS_DIR


class Story(Document):
    # --- common fields --- #
    sents = Text(analyzer="nori_analyzer")

    @classmethod
    def stream_from_corpus(cls) -> Generator['Story', None, None]:
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

    @classmethod
    def stream_from_corpus(cls) -> Generator['GK', None, None]:
        corpus_json_path = os.path.join(GK_DIR, "ko_wiki_v1_squad.json")
        with open(corpus_json_path, 'r') as fh:
            # refer to: storyteller/explore/explore_gk.py
            data = json.loads(fh.read())['data']
        for sample in data:
            for paragraph in sample['paragraphs']:
                yield cls(sents=paragraph['context'])

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

    @classmethod
    def stream_from_corpus(cls) -> Generator['SC', None, None]:
        train_json_path = os.path.join(SC_DIR, "Training", "감성대화말뭉치(최종데이터)_Training.json")
        val_json_path = os.path.join(SC_DIR, "Validation", "감성대화말뭉치(최종데이터)_Validation.json")

        for json_path in (train_json_path, val_json_path):
            with open(json_path, 'r') as fh:
                corpus_json = json.loads(fh.read())
                for sample in corpus_json:
                    yield cls(sents=" ".join(sample['talk']['content'].values()),
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

    @classmethod
    def stream_from_corpus(cls) -> Generator['MR', None, None]:
        normal_json_path = os.path.join(MR_DIR, "기계독해분야", "ko_nia_normal_squad_all.json")
        no_answer_json_path = os.path.join(MR_DIR, "기계독해분야", "ko_nia_noanswer_squad_all.json")
        clue_json_path = os.path.join(MR_DIR, "기계독해분야", "ko_nia_clue0529_squad_all.json")

        for json_path in (normal_json_path, no_answer_json_path, clue_json_path):
            with open(normal_json_path, 'r') as fh:
                corpus_json = json.loads(fh.read())
                for sample in corpus_json['data']:
                    yield cls(sents=sample['paragraphs'][0]['context'],
                              title=sample['title'])

    class Index:
        name = "mr_story"
        settings = Story.settings()


class BS(Story):
    """
    도서자료 요약
    """
    passage_id = Keyword()

    # --- additional fields for MR --- #

    @classmethod
    def stream_from_corpus(cls) -> Generator['BS', None, None]:
        json_path = os.path.join(BS_DIR, "bs.json")

        with open(json_path, 'r', encoding='UTF-8-sig') as fh:
            corpus_json = json.loads(fh.read())
            for sample in corpus_json:
                yield cls(sents=sample['passage'],
                          passage_id=sample['passage_id'])

    class Index:
        name = "bs_story"
        settings = Story.settings()


class DS(Story):
    """
    문서요약 텍스트
    """
    doc_id = Keyword()
    text_index = Keyword()

    # --- additional fields for MR --- #

    @classmethod
    def stream_from_corpus(cls) -> Generator['DS', None, None]:
        json_path = os.path.join(DS_DIR, "ds.json")

        with open(json_path, 'r', encoding='UTF-8-sig') as fh:
            corpus_jsons = json.loads(fh.read())
            for corpus_json in corpus_jsons:
                for doc in corpus_json['documents']:
                    for text in doc['text'][0]:
                        yield cls(sents=text['sentence'],
                                  doc_id=doc['id'],
                                  text_index=text['index'])

    class Index:
        name = "ds_story"
        settings = Story.settings()


class SFC(Story):
    """
    전문분야 말뭉치
    """
    doc_id = Keyword()
    sent_no = Keyword()
    title = Keyword()

    # --- additional fields for MR --- #

    @classmethod
    def stream_from_corpus(cls) -> Generator['SFC', None, None]:
        json_path = os.path.join(SFC_DIR, "sfc.json")

        with open(json_path, 'r', encoding='UTF-8-sig') as fh:
            corpus_jsons = json.loads(fh.read())

            docs = dict()
            for corpus_json in corpus_jsons:
                for doc in corpus_json['data']:
                    if 'sentence' not in doc.keys():
                        continue

                    for idx, sentence in enumerate(doc['sentence']):
                        docs[sentence['text']] = (doc['doc_id'], idx + 1)

            print("duplicates removed")
            for corpus_json in corpus_jsons:
                for doc in corpus_json['data']:
                    if 'sentence' not in doc.keys():
                        continue

                    for idx, sentence in enumerate(doc['sentence']):
                        if docs[sentence['text']] != (doc['doc_id'], idx + 1):
                            continue

                        yield cls(sents=sentence['text'],
                                  doc_id=doc['doc_id'],
                                  sent_no=idx + 1,
                                  title=doc['title'])

    class Index:
        name = "sfc_story"
        settings = Story.settings()


class KESS(Story):
    """
    한국어-영어 번역 말뭉치 사회과학
    """
    sn_id = Keyword()

    @classmethod
    def stream_from_corpus(cls) -> Generator['KESS', None, None]:
        json_path = os.path.join(KESS_DIR, "kess.json")

        with open(json_path, 'r', encoding='UTF-8-sig') as fh:
            corpus_jsons = json.loads(fh.read())
            for corpus_json in corpus_jsons:
                for doc in corpus_json['data']:
                    yield cls(sents=doc['ko'],
                              sn_id=doc['sn'])

    class Index:
        name = "kess_story"
        settings = Story.settings()


class KJ(Story):
    """
    한국어 일본어 번역 말뭉치
    """
    manage_no = Keyword()

    @classmethod
    def stream_from_corpus(cls) -> Generator['KJ', None, None]:
        json_path = os.path.join(KJ_DIR, "kj.json")

        with open(json_path, 'r', encoding='UTF-8-sig') as fh:
            corpus_jsons = json.loads(fh.read())
            for corpus_json in corpus_jsons:
                for doc in corpus_json:
                    yield cls(sents=doc['한국어'],
                              manage_no=doc['관리번호'])

    class Index:
        name = "kj_story"
        settings = Story.settings()


class KCSS(Story):
    """
    한국어 일본어 번역 말뭉치
    """
    manage_no = Keyword()

    @classmethod
    def stream_from_corpus(cls) -> Generator['KCSS', None, None]:
        json_path = os.path.join(KCSS_DIR, "kcss.json")

        with open(json_path, 'r', encoding='UTF-8-sig') as fh:
            corpus_jsons = json.loads(fh.read())
            for corpus_json in corpus_jsons:
                for doc in corpus_json:
                    yield cls(sents=doc['한국어'],
                              manage_no=doc['관리번호'])

    class Index:
        name = "kcss_story"
        settings = Story.settings()


class SFKE(Story):
    """
    전문분야 한영 말뭉치
    """
    manage_no = Keyword()

    @classmethod
    def stream_from_corpus(cls) -> Generator['SFKE', None, None]:
        json_path = os.path.join(SFKE_DIR, "sfke.json")

        with open(json_path, 'r', encoding='UTF-8-sig') as fh:
            corpus_jsons = json.loads(fh.read())
            for corpus_json in corpus_jsons:
                for doc in corpus_json:
                    yield cls(sents=doc['한국어'],
                              manage_no=doc['sid'])

    class Index:
        name = "sfke_story"
        settings = Story.settings()


class KSNS(Story):
    """
    한국어 SNS
    """
    manage_no = Keyword()

    @classmethod
    def stream_from_corpus(cls) -> Generator['KSNS', None, None]:
        json_path = os.path.join(KSNS_DIR, "ksns.json")

        with open(json_path, 'r', encoding='UTF-8-sig') as fh:
            corpus_jsons = json.loads(fh.read())
            for corpus_json in corpus_jsons:
                for doc in corpus_json:
                    yield cls(sents=doc['한국어'],
                              manage_no=doc['sid'])

    class Index:
        name = "ksns_story"
        settings = Story.settings()


class KSNS(Story):
    """
    한국어 SNS
    """
    dialogue_info = Keyword()
    utterance_id = Keyword()

    @classmethod
    def stream_from_corpus(cls) -> Generator['KSNS', None, None]:
        json_path = os.path.join(KSNS_DIR, "ksns.json")

        with open(json_path, 'r', encoding='UTF-8-sig') as fh:
            corpus_jsons = json.loads(fh.read())
            for corpus_json in corpus_jsons:
                for doc in corpus_json['data']:
                    header = doc['header']
                    body = doc['body']
                    sent = ' '.join(list(map(lambda ut: ut['utterance'], body)))

                    yield cls(sents=sent,
                              dialogue_info=header['dialogueInfo']['dialogueID'])

    class Index:
        name = "ksns_story"
        settings = Story.settings()


class KC(Story):
    """
    한국어 대화
    """
    domain_id = Keyword()
    sentence_id = Keyword()

    @classmethod
    def stream_from_corpus(cls) -> Generator['KC', None, None]:
        json_path = os.path.join(KC_DIR, "kc.json")

        with open(json_path, 'r', encoding='UTF-8-sig') as fh:
            corpus_jsons = json.loads(fh.read())
            for corpus_json in corpus_jsons:
                for doc in corpus_json:
                    if 'SENTENCE' not in doc.keys():
                        continue

                    yield cls(sents=doc['SENTENCE'],
                              domain_id=doc['DOMAINID'],
                              sentence_id=doc['SENTENCEID'])

    class Index:
        name = "kc_story"
        settings = Story.settings()


class KETS(Story):
    """
    한국어-영어 번역 말뭉치 (기술과학)
    """
    sn_id = Keyword()
    file_name = Keyword()

    @classmethod
    def stream_from_corpus(cls) -> Generator['KETS', None, None]:
        json_path = os.path.join(KETS_DIR, "kets.json")

        with open(json_path, 'r', encoding='UTF-8-sig') as fh:
            corpus_jsons = json.loads(fh.read())
            for corpus_json in corpus_jsons:
                for doc in corpus_json['data']:
                    yield cls(sents=doc['ko'],
                              sn_id=doc['sn'],
                              file_name=doc['file_name'])

    class Index:
        name = "kets_story"
        settings = Story.settings()
