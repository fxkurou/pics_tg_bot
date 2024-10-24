from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from bot.keyboards.carousel import pics_paginator, PaginationCallback
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
    photo = FSInputFile('data/search_image.jpg')
    media = InputMediaPhoto(media=photo, caption='Choose a tag to search for pictures. 🧐', parse_mode='Markdown')

    await callback.message.edit_media(media, reply_markup=tags_kb)
    await callback.answer()
    await state.set_state(SearchState.search_tags)


@search_router.callback_query(TagsCallbackFactory.filter(), StateFilter(SearchState.search_tags))
async def search_results(callback: CallbackQuery, callback_data: TagsCallbackFactory, state: FSMContext):
    tag_name = callback_data.name
    page = 0

    async with get_session() as session:
        pics = await get_pictures_by_tag(session, tag_name)

    if pics:
        pic = pics[page]
        kb = pics_paginator(page, pics)
        await callback.message.answer_photo(photo=pic.file_id, caption=pic.tag_name, reply_markup=kb)

        await state.update_data(tag_name=tag_name, page=page)
    else:
        await callback.answer('No pictures found. 😔', show_alert=True)

    await callback.answer()


@search_router.callback_query(PaginationCallback.filter() , StateFilter(SearchState.search_tags))
async def paginate(callback: CallbackQuery, callback_data: PaginationCallback, state: FSMContext):
    page = callback_data.page
    action = callback_data.action

    data = await state.get_data()
    tag_name = data.get('tag_name')
    current_page = data.get('page' , 0)


    async with get_session() as session:
        pics = await get_pictures_by_tag(session, tag_name)

    if action == 'prev' and current_page > 0:
        current_page -= 1
    elif action == 'next' and current_page < len(pics) - 1:
        current_page += 1
    elif action == 'back':
        await callback.message.answer(start, reply_markup=start_kb)
        await callback.answer()
        await state.clear()
        return

    if 0 <= current_page < len(pics):
        pic = pics[current_page]
        kb = pics_paginator(page, pics)
        media = InputMediaPhoto(media=pic.file_id)
        await callback.message.edit_media(media=media, reply_markup=kb)

        await state.update_data(page=current_page)
    else:
        await callback.answer('No pictures found. 😔', show_alert=True)
    await callback.answer()


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