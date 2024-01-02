from aiogram import types, F, Router

from config import ADMIN_ID, motya
from .query_data import RATE_DATA, LIKE_DATA, DISLIKE_DATA


router = Router(name="rating")


GROUP_NAME = "@motya_skazal"
APPROVE_KEYBOARD = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text="✅", callback_data=LIKE_DATA),
            types.InlineKeyboardButton(text="🚫", callback_data=DISLIKE_DATA),
        ]
    ],
)


@router.callback_query(F.data == RATE_DATA)
async def handle_rate(query: types.CallbackQuery):
    if isinstance(query.message, types.Message):
        await query.message.delete_reply_markup()
        txt = query.message.text or ""
        await motya.send_message(ADMIN_ID, txt, reply_markup=APPROVE_KEYBOARD)


@router.callback_query(F.data == LIKE_DATA)
async def publish_to_group(query: types.CallbackQuery):
    await motya.send_message(GROUP_NAME, query.message.text)  # type: ignore
    await query.answer(f"добавил в группу {GROUP_NAME}!")
    if isinstance(query.message, types.Message):
        await query.message.delete()


@router.callback_query(F.data == DISLIKE_DATA)
async def discard_message(query: types.CallbackQuery):
    if isinstance(query.message, types.Message):
        await query.message.delete()
