from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile

from bot.handlers.start import handle_start
from bot.states.help import HelpState
from bot.utils.commands_text import help
from bot.keyboards.help import help_kb

help_router = Router()

@help_router.callback_query(F.data == 'help')
async def handle_help(callback: CallbackQuery, state: FSMContext):
    photo = FSInputFile('data/help_image.jpg')
    media = InputMediaPhoto(media=photo, caption=help, parse_mode='Markdown')
    await callback.message.edit_media(media, reply_markup=help_kb)
    await state.set_state(HelpState.help)
    await callback.answer()


@help_router.callback_query(F.data == 'back', StateFilter(HelpState.help))
async def handle_back(callback: CallbackQuery, state: FSMContext):
    await handle_start(callback.message)
    await callback.answer()
    await state.clear()