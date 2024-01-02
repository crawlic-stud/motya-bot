import logging
from mailbox import Message
from aiogram import types, F, Router
from aiogram.exceptions import TelegramBadRequest

from config import ADMIN_ID, motya, rating_db
from .query_data import RATE_DATA, LIKE_DATA, DISLIKE_DATA


logger = logging.getLogger("rating")
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


@router.message_reaction()
async def handle_rate(message: types.MessageReactionUpdated):
    unique_id = f"{message.chat.id}.{message.message_id}"
    is_rated = rating_db.is_rated(unique_id)
    if is_rated:
        logger.info(f"Already rated message {unique_id}")
        return

    try:
        msg = await motya.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        logger.info(
            f"Forwarding message {message.message_id} from chat {message.chat.id}"
        )
    except TelegramBadRequest as e:
        logger.error(f"Error sending: {e}")
        return

    msg_text = msg.text if msg.text else "empty"
    await msg.delete()
    await motya.send_message(ADMIN_ID, msg_text, reply_markup=APPROVE_KEYBOARD)
    rating_db.add_to_rating(unique_id)


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
