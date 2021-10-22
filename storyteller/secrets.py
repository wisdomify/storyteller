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
# TODO
GCLOUD_API_KEY = ...

# --- credentials for wandb --- #
# TODO
WANDB_API_KEY = ...

