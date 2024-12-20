from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import update

from database.models import User, Picture, Tag, Donation, Payment


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

async def get_payed_pictures(session: AsyncSession):
    """Retrieve all payed pictures by a user."""
    result = await session.execute(select(Picture).options(joinedload(Picture.payment)).filter(Picture.payment_id.isnot(None)))
    return result.scalars().all()

async def create_donation(session: AsyncSession, user_id: int, order_id: str, total_amount: int, currency: str):
    """Create a new donation."""
    donation = Donation(user_id=user_id, order_id=order_id, total_amount=total_amount, currency=currency)
    session.add(donation)
    await session.commit()
    return donation

async def create_payment(session: AsyncSession, user_id: int, order_id: str, currency: str, total_amount: int):
    """Create a new payment."""
    payment = Payment(user_id=user_id, order_id=order_id, currency=currency, total_amount=total_amount)
    session.add(payment)
    await session.commit()
    return payment

async def get_nickname_by_tg_id(session: AsyncSession, tg_id: int):
    """Retrieve a user's nickname by their Telegram ID."""
    result = await session.execute(select(User).filter_by(tg_id=tg_id))
    return result.scalars().first().username

async def set_paid_true(session: AsyncSession, order_id: str):
    """Set the paid status of a picture to True."""
    await session.execute(update(Payment).where(Payment.order_id == order_id).values(paid=True))
    await session.commit()