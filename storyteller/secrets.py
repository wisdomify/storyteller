# this loads all the environment variable from .env to os.environ.
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(dotenv_path=find_dotenv())

# --- es-related --- #
ES_CLOUD_ID = os.getenv("ES_CLOUD_ID")
ES_USERNAME = os.getenv("ES_USERNAME")
ES_PASSWORD = os.getenv("ES_PASSWORD")

# --- GCP-related --- #
GCP_BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")

# --- wandb-related --- #
WANDB_API_KEY = os.getenv("WANDB_API_KEY")
WANDB_ENTITY_NAME = os.getenv("WANDB_ENTITY_NAME")
WANDB_PROJECT_NAME = os.getenv("WANDB_PROJECT_NAME")

# --- url's --- #
WISDOM2DEF_RAW_URL = os.getenv("WISDOM2DEF_RAW_URL")
WISDOMIFY_TEST_URL = os.getenv("WISDOMIFY_TEST_URL")
WISDOMS_URL = os.getenv("WISDOMS_URL")
