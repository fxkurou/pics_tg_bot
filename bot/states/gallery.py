from aiogram.fsm.state import State, StatesGroup


class GalleryState(StatesGroup):
    browse_tags = State()
