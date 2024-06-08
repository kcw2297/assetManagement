from contextlib import asynccontextmanager
from os import getenv
from typing import AsyncGenerator

import redis.asyncio as aioredis
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession

from database.config import MySQLSession
from database.enum import EnvironmentType

load_dotenv()

ENVIRONMENT = getenv("ENVIRONMENT", None)


if ENVIRONMENT == EnvironmentType.DEV:
    REDIS_HOST = getenv("LOCAL_REDIS_HOST", None)
else:
    REDIS_HOST = getenv("REDIS_HOST", None)

REDIS_PORT = int(getenv("REDIS_PORT", 6379))


@asynccontextmanager
async def get_mysql_session() -> AsyncGenerator[AsyncSession, None]:
    db = MySQLSession()
    try:
        yield db
    finally:
        await db.close()


@asynccontextmanager
async def transactional_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_mysql_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def get_redis_pool() -> aioredis.Redis:
    return aioredis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)