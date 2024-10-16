# from aiogram import Router, F
# from aiogram.filters import StateFilter
# from aiogram.types import Message
# from aiogram.fsm.context import FSMContext
#
# from bot.keyboards.back import back_kb
# from database.config import get_session
#
#
# payment_router = Router()
#
#
# @payment_router.message(F.text.casefold() == 'payment')
# async def payment(message: Message, state: FSMContext):
#     await message.answer_invoice()