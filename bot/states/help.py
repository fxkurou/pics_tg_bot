from aiogram.fsm.state import State, StatesGroup


class HelpState(StatesGroup):
    help = State()