from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.models import User, Picture, Tag


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

async def get_all_tags(session: AsyncSession):
    """Retrieve all tags from the database."""
    result = await session.execute(select(Tag))
    return result.scalars().all()

async def get_tag_by_name(session: AsyncSession, name: str):
    """Retrieve a tag by its name."""
    result = await session.execute(select(Tag).filter_by(name=name))
    return result.scalars().first()

async def create_tag(session: AsyncSession, name: str):
    """Create a new tag."""
    tag = Tag(name=name)
    session.add(tag)
    await session.commit()
    return tag

async def get_pictures_by_tag(session: AsyncSession, tag_name: str):
    """Retrieve all pictures by a tag."""
    result = await session.execute(select(Picture).filter_by(tag_name=tag_name))
    return result.scalars().all()