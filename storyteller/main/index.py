"""
index a pre-downloaded corpus into elasticsearch.
"""
import argparse
from storyteller.connectors import connect_to_es
from storyteller.elastic.docs import GK, SC, MR, BS, DS, SFC, KESS, KJ, KCSS, SFKE, KSNS
from storyteller.elastic.indexer import Indexer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index", type=str,
                        default="ksns_story")
    parser.add_argument("--batch_size", type=int,
                        default=1000)
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
    docs = {
        GK.Index.name: GK,
        SC.Index.name: SC,
        MR.Index.name: MR,
        BS.Index.name: BS,
        DS.Index.name: DS,
        SFC.Index.name: SFC,
        KESS.Index.name: KESS,
        KJ.Index.name: KJ,
        KCSS.Index.name: KCSS,
        SFKE.Index.name: SFKE,
        KSNS.Index.name: KSNS,
    }
    if index not in docs.keys():
        raise ValueError(f"Invalid index: {index}")

    docs[index].init(using=client)
    stories = docs[index].stream_from_corpus()

    # --- init an indexer with the Stories --- #
    indexer = Indexer(client, stories, index, batch_size)
    # --- index the corpus --- #
    indexer()


if __name__ == '__main__':
    main()
