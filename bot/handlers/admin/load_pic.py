import os

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from bot.filters.admin import IsAdmin
from bot.keyboards.back import back_kb
from bot.keyboards.start import start_kb
from bot.states.load_pics import LoadPicsState
from database.config import get_session
from database.models import Picture

from dotenv import load_dotenv

PICS_DIR = 'pics'

if not os.path.exists(PICS_DIR):
    os.makedirs(PICS_DIR)

load_dotenv()

admin_id = int(os.getenv('ADMIN_ID'))

load_pic_router = Router()


@load_pic_router.message(F.text.casefold() == 'upload picture', IsAdmin(admin_id))
async def upload_pic(message: Message, state: FSMContext):
    await message.answer('Send me a pic you want to upload. Type "back" to cancel.', reply_markup=back_kb)
    await state.set_state(LoadPicsState.load_pic)