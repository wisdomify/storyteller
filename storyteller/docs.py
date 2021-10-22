"""
for defining Elasticsearch docs and the indices.
"""
# each corpus has its own index.
from elasticsearch_dsl import Document, Text, Keyword


class GKDoc(Document):
    """
    일반 상식 인덱스
    """
    # --- fields for GKDoc --- #
    sents = Text(analyzer="nori")

    class Index:
        name = "gk"


class SCDoc(Document):
    """
    감성 대화 인덱스
    """
    # --- fields for SCDoc --- #
    sents = Text(analyzer="nori")
    profile_id = Keyword()
    talk_id = Keyword()

    class Index:
        name = "sc"


class MRDoc(Document):
    """
    기계 독해 인덱스
    """
    # --- fields for MRDoc --- #
    sents = Text(analyzer="nori")
    title = Keyword()

    class Index:
        name = "mr"

# class YoutoraDoc(StoriesDoc):
#     """
#     finally, Youtora project is coming back!
#     """
#     raise NotImplementedError
