from collections import Generator
from typing import List
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Document
from more_itertools import chunked
from tqdm import tqdm
from storyteller.elastic.docs import Story


class Indexer:
    """
    supports storyteller/main/index.py
    """
    def __init__(self, client: Elasticsearch,
                 stories: Generator[Story, None, None],
                 index: str,
                 batch_size: int):
        """
        :param client:
        """
        self.client = client
        self.stream = stories
        self.index = index
        self.batch_size = batch_size

    def __call__(self):
        """
        uses bulk processing in default.
        """
        for batch in tqdm(chunked(self.stream, self.batch_size),
                          desc=f"indexing {self.index}..."):
            batch: List[Document]  # a batch is a list of Document
            # must make sure include_meta is set to true, otherwise the helper won't be
            # aware of the name of the index that= we are indexing the corpus into
            actions = (doc.to_dict(include_meta=True) for doc in batch)
            r = bulk(self.client, actions)
            print(f"successful count: {r[0]}, error messages: {r[1]}")
