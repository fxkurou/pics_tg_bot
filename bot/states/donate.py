from aiogram.fsm.state import State, StatesGroup


class DonateState(StatesGroup):
    donate = State()