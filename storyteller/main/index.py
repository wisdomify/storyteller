"""
index a pre-downloaded corpus into elasticsearch.
"""
import argparse
from storyteller.connectors import connect_to_es
from storyteller.elastic.docs import GK, SC, MR, BS, DS
from storyteller.elastic.indexer import Indexer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=str,
                        default="ds_story")
    parser.add_argument("--batch_size", type=int,
                        default=500)
    # --- parse the arguments --- #
    args = parser.parse_args()
    index: str = args.index
    batch_size: int = args.batch_size
    # --- delete a previously-populated index should they exist,
    # such that we get to override it with the new mappings --- #
    client = connect_to_es()
    if client.indices.exists(index=index):
        r = client.indices.delete(index=index)
        print(f"Deleted {index} - {r}")
    # --- create the mappings for indices, and setup a stream of Stories --- #
    if index == GK.Index.name:
        GK.init(using=client)
        stories = GK.stream_from_corpus()
    elif index == SC.Index.name:
        SC.init(using=client)
        stories = SC.stream_from_corpus()
    elif index == MR.Index.name:
        MR.init(using=client)
        stories = MR.stream_from_corpus()
    elif index == BS.Index.name:
        BS.init(using=client)
        stories = BS.stream_from_corpus()
    elif index == DS.Index.name:
        DS.init(using=client)
        stories = DS.stream_from_corpus()
    else:
        raise ValueError(f"Invalid index: {index}")
    # --- init an indexer with the Stories --- #
    indexer = Indexer(client, stories, index, batch_size)
    # --- index the corpus --- #
    indexer()


if __name__ == '__main__':
    main()
