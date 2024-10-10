import os
import redis.asyncio as redis
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

redis_client = redis.from_url(redis_url, decode_responses=True)

redis_storage = RedisStorage(redis_client)