import os

from dotenv import load_dotenv

load_dotenv()

PICS_DIR = 'pics'

BOT_TOKEN = os.getenv("BOT_TOKEN")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")