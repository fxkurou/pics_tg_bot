import os

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.filters.admin import IsAdmin
from bot.filters.tag import TagValidator
from bot.keyboards.back import back_kb
from bot.keyboards.start import start_kb
from bot.states.load_pics import LoadPicsState
from database.config import get_session
from database.models import Picture

from dotenv import load_dotenv

from database.requests import get_tag_by_name, create_tag

PICS_DIR = 'pics'

if not os.path.exists(PICS_DIR):
    os.makedirs(PICS_DIR)

load_dotenv()

admin_id = int(os.getenv('ADMIN_ID'))

load_pic_router = Router()


@load_pic_router.callback_query(F.data == 'upload', IsAdmin(admin_id))
async def upload_pic(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Send me a pic you want to upload.', reply_markup=back_kb)
    await callback.answer()
    await state.set_state(LoadPicsState.load_pic)


@load_pic_router.message(F.photo, StateFilter(LoadPicsState.load_pic))
async def upload_picture(message: Message, state: FSMContext):
    picture = message.photo[-1]
    file_info = await message.bot.get_file(picture.file_id)
    file_path = file_info.file_path
    file_name = os.path.join(PICS_DIR, f"{picture.file_id}.jpg")

    await message.bot.download_file(file_path, file_name)

    await state.update_data(file_id=file_info.file_id, file_path=file_name)

    await message.answer('Send me a tag for this picture.', reply_markup=back_kb)
    await state.set_state(LoadPicsState.load_pic_tags)


@load_pic_router.message(F.text, StateFilter(LoadPicsState.load_pic_tags), TagValidator())
async def upload_picture_tag(message: Message, state: FSMContext):
    tag = message.text
    data = await state.get_data()
    file_id = data.get('file_id')
    file_path = data.get('file_path')
    user_tg_id = message.from_user.id

    async with get_session() as session:
        if await get_tag_by_name(session, tag):
            return
        else:
            await create_tag(session, tag)


    async with get_session() as session:
        picture = Picture(user_tg_id=user_tg_id, file_id=file_id, file_path=file_path, tag_name=tag)
        session.add(picture)
        await session.commit()

    await message.answer('Picture uploaded! What would u like to do now?', reply_markup=start_kb)
    await state.clear()


@load_pic_router.message(F.text.casefold() == 'back')
async def back_to_start(message: Message, state: FSMContext):
    await message.answer('What would u like to do now?', reply_markup=start_kb)
    await state.clear()


@load_pic_router.message(F.text, StateFilter(LoadPicsState.load_pic_tags))
async def handle_invalid_tag(message: Message):
    if not message.text.startswith('#'):
        await message.answer('Invalid tag. Please start with #.', reply_markup=back_kb)