"""
Credentials to be used for Authorizer.
"""
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(dotenv_path=find_dotenv())

# --- credentials for elasticsearch --- #
ES_USERNAME = os.getenv('ES_USERNAME')
ES_PASSWORD = os.getenv('ES_PASSWORD')
ES_CLOUD_ID = os.getenv('ES_CLOUD_ID')

# --- credentials for gcloud --- #
GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
# TODO
GCP_API_KEY = ...

# --- credentials for wandb --- #
WANDB_PROJECT_NAME = os.getenv("WANDB_PROJECT_NAME")
WANDB_ENTITY_NAME = os.getenv("WANDB_ENTITY_NAME")


