"""
Anything that has to do with instantiating a some sort of client (accessing .env) goes into here.
"""
from typing import Tuple
from elasticsearch import Elasticsearch
from storyteller.secrets import ES_CLOUD_ID, ES_USERNAME, ES_PASSWORD, GCLOUD_BUCKET_NAME
from google.cloud import storage
from google.cloud.storage import Client, Bucket


def connect_es() -> Elasticsearch:
    return Elasticsearch(ES_CLOUD_ID, http_auth=(ES_USERNAME, ES_PASSWORD))


def connect_gcp() -> Tuple[Client, Bucket]:
    client = storage.Client()
    bucket = client.get_bucket(GCLOUD_BUCKET_NAME)
    return client, bucket

# def connect_to_wandb():
#     pass
#
#
