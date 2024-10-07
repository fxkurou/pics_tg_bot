from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import User, Picture


async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> User:
    """Retrieve a user by their Telegram ID."""
    result = await session.execute(select(User).filter_by(tg_id=tg_id))
    return result.scalars().first()

async def register_user(session: AsyncSession, tg_id: int, username: str = None):
    """Register a new user by their Telegram ID."""
    user = User(tg_id=tg_id, username=username, is_registered=True)
    session.add(user)
    await session.commit()
    return user

async def store_picture(session: AsyncSession, user_id: int, file_id: str, file_path: str, tag: str):
    """Store a picture in the database."""
    picture = Picture(user_tg_id=user_id, file_id=file_id, file_path=file_path, tag=tag)
    session.add(picture)
    await session.commit()
    return picture