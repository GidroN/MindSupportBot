import os
import json
import socket
from dotenv import load_dotenv

hostname = socket.gethostname()

if hostname == "gidron-pc":
    filename = ".env.local"
else:
    filename = ".env.prod"

load_dotenv(filename)

BOT_TOKEN = os.getenv("BOT_TOKEN")

PG_PORT = os.getenv("PG_PORT")
PG_HOST = os.getenv("PG_HOST")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_USER = os.getenv("PG_USER")
PG_DATABASE = os.getenv("PG_DATABASE")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_PROJECT_KEY = os.getenv("OPENAI_API_PROJECT_KEY")

YANDEX_GPT_MODEL_TYPE = os.getenv("YANDEX_GPT_MODEL_TYPE")
YANDEX_GPT_CATALOG_ID = os.getenv("YANDEX_GPT_CATALOG_ID")
YANDEX_GPT_API_KEY = os.getenv("YANDEX_GPT_API_KEY")

ADMINS = json.loads(os.getenv("ADMINS", []))
