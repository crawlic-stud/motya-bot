import random
from pathlib import Path

from aiogram import Bot, types
from markovify import Text
from aiogram.utils.chat_action import ChatActionSender

from data.anekdots import ANEKDOTS_FOLDER
from .chat_history import CHAT_HISTORY_PATH, get_text_from_txt
from .markov import generate_sentence, generate_sentence_with_start
from handlers.query_data import RATE_DATA


RATE_KEYBOARD = types.InlineKeyboardMarkup(
    inline_keyboard=[[types.InlineKeyboardButton(text="💚", callback_data=RATE_DATA)]]  # type: ignore
)


def _get_anekdots_paths() -> list[Path]:
    paths = []
    for path in ANEKDOTS_FOLDER.glob("*txt"):
        if path.name.startswith("anekdots"):
            continue
        paths.append(path)
    return paths


def _get_chat_history(chat_id: int) -> str:
    path = Path(CHAT_HISTORY_PATH) / f"{chat_id}.txt"
    if not path.exists():
        return ""
    text = get_text_from_txt(path)
    return text


async def _get_text(messages: list[str], chat_id: int | str, bot: Bot) -> str:
    if not messages:
        return ""
    async with ChatActionSender.typing(bot=bot, chat_id=chat_id):
        text = "\n".join(messages)
        return text


async def random_sentence_from_messages(
    messages: list[str], chat_id: int | str, bot: Bot
) -> str:
    text = await _get_text(messages, chat_id=chat_id, bot=bot)
    sentence = generate_sentence(text)
    return sentence.lower()


async def random_sentence(messages: list[str], chat_id: int, bot: Bot) -> str:
    chat_history = _get_chat_history(chat_id)
    text = await _get_text(messages, chat_id, bot=bot)
    sentence = generate_sentence(text + chat_history)
    return sentence.lower()


async def random_sentence_with_start(
    starts: list[str], messages: list[str], chat_id: int, bot: Bot
) -> str:
    chat_history = _get_chat_history(chat_id)
    text = await _get_text(messages, chat_id, bot)
    start = random.choice(starts)
    sentence = generate_sentence_with_start(text + chat_history, keyword=start)
    return sentence.lower()


async def random_anekdot(state_size=3) -> str:
    paths = _get_anekdots_paths()
    theme = random.choice(paths)
    model = Text(
        theme.read_text(encoding="utf-8"), well_formed=True, state_size=state_size
    )
    sentence = model.make_sentence(tries=1000) or ""
    return sentence.lower()


async def reply_with_kb(message: types.Message, text: str):
    return await message.reply(text)
    # return await message.reply(text, reply_markup=RATE_KEYBOARD)


async def answer_with_kb(message: types.Message, text: str):
    return await message.answer(text)
    # return await message.answer(text, reply_markup=RATE_KEYBOARD)
