from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

from bot.handlers.start import handle_start
from bot.keyboards.carousel import pics_paginator, PaginationCallback
from bot.keyboards.tags import get_tags_kb, TagsCallbackFactory, TagsPaginationCallbackFactory
from bot.states.gallery import GalleryState

from database.config import get_session
from database.requests import get_pictures_by_tag, get_all_tags

gallery_router = Router()


@gallery_router.callback_query(F.data == 'gallery')
async def handle_gallery(callback: CallbackQuery, state: FSMContext):
    async with get_session() as session:
        tags = await get_all_tags(session)
    tags_kb = await get_tags_kb(tags, page=0)
    photo = FSInputFile('data/gallery_image.jpg')
    media = InputMediaPhoto(media=photo, caption='Choose a tag to browse for. 🧐', parse_mode='Markdown')

    try:
        await callback.message.edit_media(media, reply_markup=tags_kb)
    except Exception:
        await callback.answer('Choose a tag to browse for. 😊', show_alert=True)

    await callback.answer()
    await state.set_state(GalleryState.browse_tags)


@gallery_router.callback_query(TagsCallbackFactory.filter(), StateFilter(GalleryState.browse_tags))
async def handle_gallery_results(callback: CallbackQuery, callback_data: TagsCallbackFactory, state: FSMContext):
    tag_name = callback_data.name
    page = 0

    async with get_session() as session:
        pics = await get_pictures_by_tag(session, tag_name)

    if pics:
        pic = pics[page]
        kb = pics_paginator(page, pics)
        media = InputMediaPhoto(media=pic.file_id)
        await callback.message.edit_media(media=media, caption=pic.tag_name, reply_markup=kb)

        await state.update_data(tag_name=tag_name, page=page)
    else:
        await callback.message.edit_caption('No pictures found. 😔')

    await callback.answer()


@gallery_router.callback_query(TagsPaginationCallbackFactory.filter())
async def handle_tags_pagination(callback: CallbackQuery, callback_data: TagsPaginationCallbackFactory):
    page = callback_data.page

    async with get_session() as session:
        tags = await get_all_tags(session)

    tags_kb = await get_tags_kb(tags, page=page)

    await callback.message.edit_reply_markup(reply_markup=tags_kb)
    await callback.answer()


@gallery_router.callback_query(PaginationCallback.filter() , StateFilter(GalleryState.browse_tags))
async def handle_paginate_pics(callback: CallbackQuery, callback_data: PaginationCallback, state: FSMContext):
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
        await handle_gallery(callback, state)
        await callback.answer()
        await state.set_state(GalleryState.browse_tags)
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


@gallery_router.message(StateFilter(GalleryState.browse_tags))
async def handle_wrong_input(message: Message, state: FSMContext):
    await message.answer('Please use the buttons to choose a tag. 🙏 \n'
                         'Or press "Back" to go back to the main menu.', reply_markup=ReplyKeyboardRemove())
    await state.set_state(GalleryState.browse_tags)


@gallery_router.callback_query(F.data == 'back', StateFilter(GalleryState.browse_tags))
async def handle_go_back(callback: CallbackQuery, state: FSMContext):
    await handle_start(callback.message)
    await callback.answer()
    await state.clear()
