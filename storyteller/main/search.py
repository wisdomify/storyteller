"""
searches for a wisdom from a given
"""
import argparse
from elasticsearch import Elasticsearch
from storyteller.connectors import connect_es


class Searcher:
    """
    supports storyteller/main/search.py
    """
    def __init__(self, client: Elasticsearch):
        self.client = client

    def __call__(self, wisdom: str, indices: str,  size: int) -> dict:
        query = {
            'match_phrase': {
                'sents': {
                    'query': wisdom,
                    'analyzer': 'nori'
                }
             }
         }
        highlight = {
            'fields': {
                'sents': {
                    'type': 'plain',
                    'fragment_size': 100,
                    'number_of_fragments': 2,
                    'fragmenter': 'span'
                }
            }
         }
        return self.client.search(index=indices, query=query, highlight=highlight, size=size, )


# --- the script --- #
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--w", type=str,
                        default="어")
    parser.add_argument("--i", type=str,
                        # just comma-enumerate the indices for multi-indices search
                        # https://www.elastic.co/guide/en/elasticsearch/reference/current/search-multiple-indices.html
                        default="gk,sc,mr")
    parser.add_argument("--s", type=int,
                        # 10000 is the maximum
                        default=10000)
    args = parser.parse_args()
    wisdom: str = args.w
    indices: str = args.i
    size: int = args.s
    # --- instantiate a searcher --- #
    searcher = Searcher(connect_es())
    res = searcher(wisdom, indices, size)
    for hit in res['hits']['hits']:
        # also display which indices it came from
        print(f"indices: {hit['_index']}, highlight:{hit['highlight']['sents'][0]}")


if __name__ == '__main__':
    main()
