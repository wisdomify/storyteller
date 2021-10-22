import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())

# Elastic Search credentials
ES_USER = os.getenv('es_user')
ES_PASSWORD = os.getenv('es_password')
