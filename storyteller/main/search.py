"""
searches for
"""
import argparse
from storyteller.connectors import connect_to_es
from storyteller.elastic.crud import Searcher
from storyteller.elastic.docs import Story


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--wisdom", type=str,
                        # why can't I search for stopwords?
                        default="꿩 대신 닭")
    parser.add_argument("--index", type=str,
                        # just comma-enumerate the indices for multi-indices search
                        # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-multiple-indices.html
                        default=",".join(Story.all_indices()))
    parser.add_argument("--size", type=int,
                        # 10000 is the maximum
                        default=10000)
    args = parser.parse_args()
    wisdom: str = args.wisdom
    index: str = args.index
    size: int = args.size
    # --- instantiate a searcher --- #
    searcher = Searcher(connect_to_es())
    res = searcher(wisdom, index, size)
    print(res['hits']['total'])
    for hit in res['hits']['hits']:
        # also display which indices it came from
        print(f"indices: {hit['_index']}, highlight:{hit['highlight']['sents'][0]}")


if __name__ == '__main__':
    main()
