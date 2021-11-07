"""
Anything that has to do with instantiating some sort of  a client via acessing .env,
goes into here.
"""
import wandb
from wandb.sdk.wandb_run import Run
from typing import Tuple
from elasticsearch import Elasticsearch
from storyteller.paths import DATA_DIR
from storyteller.secrets import (
    ES_USERNAME,
    ES_PASSWORD,
    ES_CLOUD_ID,
    GCP_BUCKET_NAME,
    WANDB_ENTITY_NAME,
    WANDB_PROJECT_NAME
)
from google.cloud import storage
from google.cloud.storage import Client, Bucket


# --- elasticsearch --- #
def connect_to_es() -> Elasticsearch:
    es = Elasticsearch(ES_CLOUD_ID, http_auth=(ES_USERNAME, ES_PASSWORD))
    return es


# --- google cloud platform --- #
def connect_to_gcp() -> Tuple[Client, Bucket]:
    client = storage.Client()
    bucket = client.get_bucket(GCP_BUCKET_NAME)
    return client, bucket


# --- weights & biases --- #
def connect_to_wandb(**kwargs) -> Run:
    run = wandb.init(dir=DATA_DIR,
                     project=WANDB_PROJECT_NAME,
                     entity=WANDB_ENTITY_NAME,
                     **kwargs)
    return run
