from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from dotenv import load_dotenv
import os

from database.models import Base

load_dotenv()

engine = create_async_engine(
    f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    f"?async_fallback=True",
    echo=True,
)

session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@asynccontextmanager
async def get_session():
    """
    Get session for database operations in async function or context manager.

    :return: None
    """
    async with session_maker() as session:
        yield session


async def init_db() -> None:
    """
    Create tables in database.

    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)