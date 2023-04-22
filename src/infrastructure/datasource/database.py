import functools
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.config import get_settings

Base = declarative_base()

async_engine = create_async_engine(get_settings().DATABASE_URL, echo=False)
# AsyncSessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=async_engine,
#     class_=AsyncSession,
#     future=True,
# )
AsyncSessionLocal = async_sessionmaker(async_engine)


async def get_db_async() -> AsyncGenerator:
    async with AsyncSessionLocal.begin() as async_session:
        try:
            await async_session.execute(text(f"SET search_path TO {get_settings().DATABASE_SCHEMA}"))
            yield async_session
            await async_session.commit()
        except Exception:
            await async_session.rollback()
        finally:
            await async_session.close()


def db_connection():  # noqa
    def wrapper(func):  # noqa
        @functools.wraps(func)  # noqa
        async def wrapped(*args):  # noqa
            async_generator = get_db_async()
            while True:
                try:
                    async_session = await async_generator.__anext__()
                    await func(*args, async_session=async_session)
                except StopAsyncIteration:
                    break

        return wrapped

    return wrapper
