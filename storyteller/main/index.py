"""
index a pre-downloaded corpus into elasticsearch.
"""
import argparse
from typing import List
from elasticsearch import Elasticsearch
from elasticsearch.helpers.actions import bulk
from elasticsearch_dsl import Document
from more_itertools import chunked
from storyteller.connectors import connect_to_es
from storyteller.docs import GKDoc, SCDoc, MRDoc
from storyteller.readers import GKReader, SCReader, Reader, MRReader
from tqdm import tqdm


class Indexer:
    """
    supports storyteller/main/index.py
    """
    def __init__(self, client: Elasticsearch):
        """
        :param client:
        """
        self.client = client

    def __call__(self, reader: Reader, index: str, batch_size: int):
        """
        uses bulk processing in default.
        """
        for batch in tqdm(chunked(reader, batch_size), desc=f"indexing {index}..."):
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
    # --- delete a previously-populated index (for overriding with the new one)--- #
    client = connect_to_es()
    r = client.indices.delete(index=index)
    print(f"deleting {index} - {r}")
    if index == "gk":
        GKDoc.init(using=client)  # create mappings
        reader = GKReader()  # instantiate the reader
    elif index == "sc":
        SCDoc.init(using=client)
        reader = SCReader()
    elif index == "mr":
        MRDoc.init(using=client)
        reader = MRReader()
    else:
        raise ValueError(f"Invalid index: {index}")
    # --- init an indexer --- #
    indexer = Indexer(client)
    # --- index the corpus --- #
    indexer(reader=reader, index=index, batch_size=batch_size)


if __name__ == '__main__':
    main()
