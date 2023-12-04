from aiogram import types

from config import dp, ADMIN_ID, motya
from .query_data import RATE_DATA, LIKE_DATA, DISLIKE_DATA


GROUP_NAME = "@motya_skazal"
APPROVE_KEYBOARD = types.InlineKeyboardMarkup(2).add(
    types.InlineKeyboardButton("✅", callback_data=LIKE_DATA),  # type: ignore
    types.InlineKeyboardButton("🚫", callback_data=DISLIKE_DATA),  # type: ignore
)


@dp.callback_query_handler(lambda c: c.data == RATE_DATA)
async def handle_rate(query: types.CallbackQuery):
    await query.message.delete_reply_markup()
    await motya.send_message(
        ADMIN_ID, query.message.text, reply_markup=APPROVE_KEYBOARD
    )


@dp.callback_query_handler(lambda c: c.data == LIKE_DATA)
async def publish_to_group(query: types.CallbackQuery):
    await motya.send_message(GROUP_NAME, query.message.text)
    await query.answer(f"добавил в группу {GROUP_NAME}!")
    await query.message.delete()


@dp.callback_query_handler(lambda c: c.data == DISLIKE_DATA)
async def discard_message(query: types.CallbackQuery):
    await query.message.delete()
