"""
index a pre-downloaded corpus into elasticsearch.
"""
import argparse
from storyteller.connectors import connect_to_es
from storyteller.elastic.docs import GK, SC, MR, Story
from storyteller.elastic.indexer import Indexer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--i", type=str,
                        default="gk")
    parser.add_argument("--b", type=int,
                        default=1000)
    # --- parse the arguments --- #
    args = parser.parse_args()
    index: str = args.i
    batch_size: int = args.b
    # --- delete a previously-populated index should they exist,
    # such that we get to override it with the new mappings --- #
    client = connect_to_es()
    if client.indices.exists(index=index):
        r = client.indices.delete(index=index)
        print(f"deleting {index} - {r}")
    # --- create the mappings for indices, and setup a stream of Stories --- #
    if index == "gk":
        GK.init(using=client)
        stories = GK.stream_from_corpus()
    elif index == "sc":
        SC.init(using=client)
        stories = SC.stream_from_corpus()
    elif index == "mr":
        MR.init(using=client)
        stories = MR.stream_from_corpus()
    else:
        raise ValueError(f"Invalid index: {index}")
    # --- init an indexer with the Stories --- #
    indexer = Indexer(client, stories, index, batch_size)
    # --- index the corpus --- #
    indexer()


if __name__ == '__main__':
    main()
