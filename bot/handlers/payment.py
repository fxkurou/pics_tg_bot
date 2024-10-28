from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.config import get_session
from bot.config import PAYMENTS_PROVIDER_TOKEN

PAYMENTS_PROVIDER_TOKEN = PAYMENTS_PROVIDER_TOKEN

payment_router = Router()


