import json
from typing import List, Dict, Union

from elasticsearch import Elasticsearch


class ElasticController:
    def __init__(self,
                 cloud_id: str,
                 user_id: str,
                 user_pw: str,
                 index_name: str):
        self.elastic = Elasticsearch(cloud_id, http_auth=(user_id, user_pw))
        self.index = index_name

        self.batch_size = 10000

    def read(self,
             query: dict,
             highlight: dict = None):
        """
        :param query:
        :param highlight:
        '''
        >>> # Example input parameter
        >>> query = {
        >>>     'match_phrase': {
        >>>         'eg': {
        >>>             'query': query,
        >>>             'analyzer': 'nori'
        >>>         }
        >>>     }
        >>> }
        >>> highlight = {
        >>>     'fields': {
        >>>         'eg': {
        >>>             'type': 'plain',
        >>>             'fragment_size': 15,
        >>>             'number_of_fragments': 2,
        >>>             'fragmenter': 'span'
        >>>         }
        >>>     }
        >>> }
        '''
        :return:
        """
        return self.elastic.search(index=self.index, query=query, highlight=highlight)

    def write(self,
              info: Union[List[Dict], Dict],
              bulk: bool):
        """
        :param bulk:
        :param info:
        :return:
        """
        if bulk:
            if type(info) != list:
                raise ValueError("Invalid info: (bulk is True) info must be List of dictionary.")
        else:
            if type(info) != dict:
                raise ValueError("Invalid info: (bulk is True) info must be List of dictionary.")

        if bulk:
            res = list()

            for d in range((len(info) // self.batch_size) + 1):
                cur_docs = info[d * self.batch_size: (d + 1) * self.batch_size]
                cur_docs = '\n'.join(
                    list(
                        map(
                            lambda doc: '{"index": {}}\n' + json.dumps(doc),
                            cur_docs
                        )
                    )
                )

                r = self.elastic.bulk(index=self.index, doc_type='_doc', body=cur_docs)
                res.append(r)

            return res

        else:
            return self.elastic.index(index=self.index, doc_type='_doc', document=info)
