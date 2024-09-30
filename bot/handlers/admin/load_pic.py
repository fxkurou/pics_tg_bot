from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.states.load_pics import LoadPicsState
from database.config import get_session
from database.models import Picture

load_pic_router = Router()

@load_pic_router.message(F.text=='Upload pic')
async def upload_pic(message : Message, state: FSMContext):
    await message.answer('Send me a pic you want to upload')
    await state.set_state(LoadPicsState.load_pic)


@load_pic_router.message(StateFilter(LoadPicsState.load_pic))
async def handle_photo_upload(message: Message, state: FSMContext):
    pic = message.photo[-1]  # Get the highest resolution photo
    file_info = await message.bot.get_file(pic.file_id)
    file_path = file_info.file_path

    # Download the photo from Telegram
    pic_data = await message.bot.download_file(file_path)

    # Store the photo temporarily in the FSM context
    await state.update_data(pic_data=pic_data.getvalue(), id=pic.file_id)

    # Ask the user for tags
    await message.reply("Pic received! Now, please send me some tags for this pic.")
    await state.set_state(LoadPicsState.load_pic_tags)  # Move to the next state to receive tags


@load_pic_router.message(StateFilter(LoadPicsState.load_pic_tags))
async def handle_tags(message: Message, state: FSMContext):
    tags = message.text  # The user input for tags

    # Retrieve the stored photo data from the FSM context
    data = await state.get_data()
    user_tg_id = message.from_user.id
    file_id = data.get('id')
    file_path = data.get('file_path')

    # Save the photo and tags to the database
    async with get_session() as session:
        new_photo = Picture(
            id=file_id,
            file_name=f'{file_id}.jpg',
            user_tg_id=user_tg_id,
            tag=tags,
            file_path=file_path
        )
        session.add(new_photo)
        await session.commit()

    # Notify the user that the upload is complete
    await message.reply(f"Your photo has been uploaded with tags: {tags}")