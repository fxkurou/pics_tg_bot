from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, FSInputFile, InputMediaPhoto, LabeledPrice, PreCheckoutQuery, Message
from aiogram.fsm.context import FSMContext

from bot.handlers.start import get_start
from bot.keyboards.payment import get_payment_kb, PaymentCallbackFactory
from database.config import get_session
from bot.config import PAYMENTS_PROVIDER_TOKEN
from database.requests import get_payed_pictures, get_nickname_by_tg_id

PAYMENTS_PROVIDER_TOKEN = PAYMENTS_PROVIDER_TOKEN

payment_router = Router()


@payment_router.callback_query(F.data == 'creators')
async def handle_creators(callback: CallbackQuery):
    page = 0
    async with get_session() as session:
        pics = await get_payed_pictures(session)
        nickname = await get_nickname_by_tg_id(session, callback.from_user.id)

    if pics:
        pic = pics[page]
        kb = get_payment_kb(amount=pic.payment.total_amount, page=page, items=pics)

        media = InputMediaPhoto(
            media=pic.file_id,
            caption=f'Creator: @{nickname}\n{pic.tag_name}',
            parse_mode='Markdown'
        )
        await callback.message.edit_media(media=media, reply_markup=kb)
    else:
        await callback.message.answer("No pictures available at the moment.")

    await callback.answer()

@payment_router.callback_query(PaymentCallbackFactory.filter())
async def handle_payment_actions(callback: CallbackQuery, callback_data: PaymentCallbackFactory):
    action = callback_data.action
    page = callback_data.page
    amount = callback_data.amount

    async with get_session() as session:
        pics = await get_payed_pictures(session)
        nickname = await get_nickname_by_tg_id(session, callback.from_user.id)

    if action in ['prev', 'next']:
        pic = pics[page]
        kb = get_payment_kb(amount=pic.payment.total_amount, page=page, items=pics)

        media = InputMediaPhoto(
            media=pic.file_id,
            caption=f'Creator: @{nickname}\n{pic.tag_name}',
            parse_mode='Markdown'
        )
        await callback.message.edit_media(media=media, reply_markup=kb)

    elif action == 'pay':
        pic = pics[page]
        await callback.message.answer_invoice(
            need_phone_number=True,
            title="Support the creator",
            description=f'Creator: @{nickname}\n{pic.tag_name}',
            payload='test_payload',
            provider_token=PAYMENTS_PROVIDER_TOKEN,
            currency="USD",
            prices=[LabeledPrice(label="Amount", amount=pic.payment.total_amount * 100)],
        )

    elif action == 'back':
        await get_start(callback.message)

    await callback.answer()

@payment_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@payment_router.message(F.successful_payment())
async def process_successful_payment(message: Message):
    await message.answer('Thank you for your support! 🥰')
    await get_start(message)
