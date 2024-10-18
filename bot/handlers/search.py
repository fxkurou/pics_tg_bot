from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from bot.keyboards.start import start_kb
from bot.keyboards.tags import get_tags_kb, TagsCallbackFactory
from bot.states.search import SearchState
from bot.utils.commands_text import start
from database.config import get_session

from database.requests import get_pictures_by_tag, get_all_tags

search_router = Router()


@search_router.callback_query(F.data == 'search')
async def search(callback: CallbackQuery, state: FSMContext):
    async with get_session() as session:
        tags = await get_all_tags(session)
    tags_kb = await get_tags_kb(tags)
    await callback.message.edit_text('Choose a tag to search for:', reply_markup=tags_kb)
    await callback.answer()
    await state.set_state(SearchState.search_tags)


@search_router.callback_query(TagsCallbackFactory.filter(), StateFilter(SearchState.search_tags))
async def search_results(callback: CallbackQuery, callback_data: TagsCallbackFactory, state: FSMContext):
    tag_name = callback_data.name

    await callback.message.answer('Here are the results:', reply_markup=ReplyKeyboardRemove())
    async with get_session() as session:
        pics = await get_pictures_by_tag(session, tag_name)

    for pic in pics:
        await callback.message.answer_photo(photo=pic.file_id, caption=pic.tag_name)
    await callback.message.answer(start, reply_markup=start_kb)
    await callback.answer()
    await state.set_state(SearchState.search_tags)


@search_router.message(StateFilter(SearchState.search_tags))
async def search_results(message: Message, state: FSMContext):
    await message.answer('Please use the buttons to choose a tag. 🙏 \n'
                         'Or press "Back" to go back to the main menu.', reply_markup=ReplyKeyboardRemove())
    await state.set_state(SearchState.search_tags)


@search_router.callback_query(F.data == 'back', StateFilter(SearchState.search_tags))
async def go_back(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(start, reply_markup=start_kb)
    await callback.answer()
    await state.clear()