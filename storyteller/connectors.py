from elasticsearch import Elasticsearch
from storyteller.secrets import ES_CLOUD_ID, ES_USERNAME, ES_PASSWORD


def connect_to_es() -> Elasticsearch:
    return Elasticsearch(ES_CLOUD_ID, http_auth=(ES_USERNAME, ES_PASSWORD))


# def connect_to_wandb():
#     pass
#
#
# def connect_to_gcp():
#     pass
#
