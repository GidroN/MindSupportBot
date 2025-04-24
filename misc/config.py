import os
import socket
from dotenv import load_dotenv
from redis.asyncio.client import Redis

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

redis_instance = Redis(host=REDIS_HOST, port=int(REDIS_PORT))
