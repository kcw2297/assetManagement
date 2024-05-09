from os import getenv

from dotenv import load_dotenv
from redis import Redis

from database.config import AsyncDBSession, MySQLSession

load_dotenv()

REDIS_HOST = getenv("REDIS_HOST", None)
REDIS_PORT = getenv("REDIS_PORT", None)


async def get_mysql_async_session():
    db = AsyncDBSession()
    try:
        yield db
    finally:
        db.close()


def get_mysql_session():
    db = MySQLSession()
    try:
        yield db
    finally:
        db.close()


def get_redis_pool() -> Redis:
    return Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)