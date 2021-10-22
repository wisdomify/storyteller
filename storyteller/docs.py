"""
for defining Elasticsearch docs and the indices.
"""
# each corpus has its own index.
from elasticsearch_dsl import Document, Text, Keyword


# --- to be used to define the settings --- #
def settings() -> dict:
    """
    https://prohannah.tistory.com/73
    https://coding-start.tistory.com/167
    :return:
    """
    return {
            "analysis": {
                "tokenizer": {
                    "my_nori_tokenizer": {
                        "type": "nori_tokenizer",
                        # 마곡역 -> 마곡역, 마곡, 역
                        "decompound_mode": "mixed",
                    }
                },
                "analyzer": {
                    "my_nori_analyzer": {
                        "tokenizer": "my_nori_tokenizer",
                        "filter": [
                            "my_nori_filter"
                        ]
                    }
                },
                "filter": {
                    "my_nori_filter": {
                        "type": "nori_part_of_speech",
                        # 공백외에 전부 허용 - 이걸.. 어떻게 하지..
                        "stoptags": ["SP"]
                    }
                }
            }
        }


class GKDoc(Document):
    """
    일반 상식 인덱스
    """
    # --- fields for GKDoc --- #
    sents = Text(analyzer="nori_analyzer")

    class Index:
        name = "gk"
        settings = settings()


class SCDoc(Document):
    """
    감성 대화 인덱스
    """
    # --- fields for SCDoc --- #
    sents = Text(analyzer="nori_analyzer")
    profile_id = Keyword()
    talk_id = Keyword()

    class Index:
        name = "sc"
        settings = settings()


class MRDoc(Document):
    """
    기계 독해 인덱스
    """
    # --- fields for MRDoc --- #
    sents = Text(analyzer="nori")
    title = Keyword()

    class Index:
        name = "mr"
        settings = settings()

# class YoutoraDoc(StoriesDoc):
#     """
#     finally, Youtora project is coming back!
#     """
#     raise NotImplementedError
