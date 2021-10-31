"""
searches for
"""
import argparse
from storyteller.connectors import connect_to_es
from storyteller.elastic.searcher import Searcher
from storyteller.elastic.docs import Story


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--w", type=str,
                        # why can't I search for stopwords?
                        default="산 넘어 산")
    parser.add_argument("--i", type=str,
                        # just comma-enumerate the indices for multi-indices search
                        # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-multiple-indices.html
                        default=",".join([cls.Index.name for cls in Story.__subclasses__()]))
    parser.add_argument("--s", type=int,
                        # 10000 is the maximum
                        default=10000)
    args = parser.parse_args()
    wisdom: str = args.w
    indices: str = args.i
    size: int = args.s
    # --- instantiate a searcher --- #
    searcher = Searcher(connect_to_es())
    res = searcher(wisdom, indices, size)
    print(res['hits']['total'])
    for hit in res['hits']['hits']:
        # also display which indices it came from
        print(f"indices: {hit['_index']}, highlight:{hit['highlight']['sents'][0]}")


if __name__ == '__main__':
    main()
