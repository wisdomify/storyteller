"""
Anything that has to do with instantiating a some sort of client (accessing .env) goes into here.
"""
import wandb
from wandb.sdk.wandb_run import Run
from typing import Tuple
from elasticsearch import Elasticsearch
from storyteller.paths import DATA_DIR
from storyteller.secrets import ES_CLOUD_ID, ES_USERNAME, ES_PASSWORD, GCP_BUCKET_NAME, WANDB_PROJECT_NAME, \
    WANDB_ENTITY_NAME
from google.cloud import storage
from google.cloud.storage import Client, Bucket


def connect_es() -> Elasticsearch:
    es = Elasticsearch(ES_CLOUD_ID, http_auth=(ES_USERNAME, ES_PASSWORD))
    return es


def connect_gcp() -> Tuple[Client, Bucket]:
    client = storage.Client()
    bucket = client.get_bucket(GCP_BUCKET_NAME)
    return client, bucket


def connect_wandb(**kwargs) -> Run:
    run = wandb.init(dir=DATA_DIR,
                     project=WANDB_PROJECT_NAME,
                     entity=WANDB_ENTITY_NAME,
                     **kwargs)
    return run
