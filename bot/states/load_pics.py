from aiogram.fsm.state import State, StatesGroup


class LoadPicsState(StatesGroup):
    load_pic = State()
    load_pic_tags = State()