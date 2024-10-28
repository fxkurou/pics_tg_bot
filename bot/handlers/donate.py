from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery
from aiogram.fsm.context import FSMContext

from bot.handlers.start import get_start
from database.config import get_session
from bot.utils.commands_text import donate as start_donate_text
from bot.keyboards.donate import get_donate_kb, DonateCallbackFactory, invoice_kb
from database.requests import create_donation

donate_router = Router()


@donate_router.callback_query(F.data == "donate")
async def donate(callback: CallbackQuery, state: FSMContext):
    kb = await get_donate_kb()
    await callback.message.edit_caption(caption=start_donate_text, parse_mode="None", reply_markup=kb)
    await state.set_state("donate")


@donate_router.callback_query(DonateCallbackFactory.filter(), StateFilter("donate"))
async def process_donation(callback: CallbackQuery, callback_data: DonateCallbackFactory):
    amount = callback_data.amount
    prices = [LabeledPrice(label=f"{amount} stars", amount=amount)]
    kb = await invoice_kb(amount)

    await callback.bot.send_invoice(
        chat_id=callback.from_user.id,
        title="Support the creator",
        description=f"Donation of {amount} stars",
        payload=f"{amount}_stars",
        provider_token="",
        currency="XTR",
        prices=prices,
        reply_markup=kb
    )
    await callback.answer()


@donate_router.pre_checkout_query()
async def on_pre_checkout_query(pre_checkout_query: PreCheckoutQuery, state: FSMContext):
    await pre_checkout_query.answer(ok=True)
    await state.update_data(invoice_payload=pre_checkout_query)


@donate_router.callback_query(F.successful_payment)
async def on_successful_payment(callback: CallbackQuery, state: FSMContext):
    order_id = callback.successful_payment.telegram_payment_charge_id
    await callback.message.answer(
        'Thank you for your donation! 🎉\n' 
        'Your support is greatly appreciated! ❤️\n'
        f'Here is the transaction ID: {order_id}'
        )
    data = await state.get_data()
    total_amount = data.get("total_amount")
    currency = data.get("currency")

    async with get_session() as session:
        await create_donation(
            session,
            callback.from_user.id,
            order_id,
            total_amount,
            currency
        )

    await get_start(callback.message)
    await state.clear()
    await callback.answer()


@donate_router.callback_query(F.data == "back", StateFilter("donate"))
async def back(callback: CallbackQuery, state: FSMContext):
    await get_start(callback.message)
    await state.clear()
    await callback.answer()