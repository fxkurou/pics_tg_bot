import os

from aiogram import Bot
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv

from bot.keyboards.start import start_kb
from bot.utils.commands_text import start
from database.requests import register_user, get_user_by_tg_id
from database.config import get_session, init_db

load_dotenv()

ADMIN_ID = int(os.getenv('ADMIN_ID'))

start_router = Router()


@start_router.startup()
async def on_startup(bot: Bot) -> None:
    await init_db()
    await bot.send_message(chat_id=ADMIN_ID, text='Bot started')


@start_router.message(CommandStart())
async def get_start(message: Message):
    tg_id = message.from_user.id
    username = message.from_user.username

    async with get_session() as session:
        try:
            user = await get_user_by_tg_id(session, tg_id)
            photo = FSInputFile('data/start_image.jpg')

            if not user:
                await register_user(session, tg_id, username)

            await message.answer_photo(photo, start, reply_markup=start_kb)

        finally:
            await session.close()

