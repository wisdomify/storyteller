"""
index a pre-downloaded corpus into elasticsearch.
"""
import argparse
from typing import List, Generator
from elasticsearch import Elasticsearch
from elasticsearch.helpers.actions import bulk
from elasticsearch_dsl import Document
from more_itertools import chunked
from storyteller.connectors import connect_es
from storyteller.docs import GK, SC, MR, Story
from tqdm import tqdm


class Indexer:
    """
    supports storyteller/main/index.py
    """
    def __init__(self, client: Elasticsearch,
                 stream: Generator[Story, None, None],
                 index: str,
                 batch_size: int):
        """
        :param client:
        """
        self.client = client
        self.stream = stream
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


# --- the script --- #
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--i", type=str,
                        default="mr")
    parser.add_argument("--b", type=int,
                        default=1000)
    # --- parse the arguments --- #
    args = parser.parse_args()
    index: str = args.i
    batch_size: int = args.b
    # --- delete a previously-populated index should they exist, so that we can override with the new one --- #
    client = connect_es()
    if client.indices.exists(index=index):
        r = client.indices.delete(index=index)
        print(f"deleting {index} - {r}")
    # --- create the mappings for indices, and setup a stream of Story's --- #
    if index == "gk":
        GK.init(using=client)
        stream = GK.from_corpus()
    elif index == "sc":
        SC.init(using=client)
        stream = SC.from_corpus()
    elif index == "mr":
        MR.init(using=client)
        stream = MR.from_corpus()
    else:
        raise ValueError(f"Invalid index: {index}")
    # --- init an indexer with the Story's --- #
    indexer = Indexer(client, stream, index, batch_size)
    # --- index the corpus --- #
    indexer()


if __name__ == '__main__':
    main()
