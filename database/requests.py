from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import User

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
