import os

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.filters.tag import TagValidator
from bot.keyboards.back import back_kb
from bot.keyboards.start import start_kb
from bot.states.search import SearchState
from database.config import get_session

from database.requests import get_tag_by_name, get_pictures_by_tag

search_router = Router()


@search_router.message(F.text.casefold() == 'search')
async def search(message: Message, state: FSMContext):
    await message.answer('Send me a tag you want to search for.', reply_markup=back_kb)
    await state.set_state(SearchState.search_tags)


@search_router.message(F.text, StateFilter(SearchState.search_tags), TagValidator())
async def search_results(message: Message, state: FSMContext):
    tag_name = message.text
    async with get_session() as session:
        tag = await get_tag_by_name(session, tag_name)

    if tag is None:
        await message.answer('Tag does not exist. Try another one.', reply_markup=back_kb)
        await state.set_state(SearchState.search_tags)
    else:
        await message.answer('Here are the results:', reply_markup=back_kb)
        async with get_session() as session:
            pics = await get_pictures_by_tag(session, tag_name)
        for pic in pics:
            await message.answer_photo(photo=pic.file_id, caption=pic.tag_name)
        await message.answer('Send me another tag you want to search for or press "back" to return to start menu.',
                             reply_markup=back_kb)
        await state.set_state(SearchState.search_tags)