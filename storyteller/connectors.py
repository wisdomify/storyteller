"""
Anything that has to do with instantiating some sort of  a client via acessing .env,
goes into here.
"""
import wandb
import os
from wandb.sdk.wandb_run import Run
from typing import Tuple
from elasticsearch import Elasticsearch
from storyteller.paths import DATA_DIR
from google.cloud import storage
from google.cloud.storage import Client, Bucket


# --- elasticsearch --- #
def connect_to_es() -> Elasticsearch:
    es = Elasticsearch(os.getenv("ES_CLOUD_ID"), http_auth=(os.getenv("ES_USERNAME"),
                                                            os.getenv("ES_PASSWORD")))
    return es


# --- google cloud platform --- #
def connect_to_gcp() -> Tuple[Client, Bucket]:
    client = storage.Client()
    bucket = client.get_bucket(os.getenv("GCP_BUCKET_NAME"))
    return client, bucket


# --- weights & biases --- #
def connect_to_wandb(**kwargs) -> Run:
    run = wandb.init(dir=DATA_DIR,
                     project=os.getenv("WANDB_PROJECT_NAME"),
                     entity=os.getenv("WANDB_ENTITY_NAME"),
                     **kwargs)
    return run
