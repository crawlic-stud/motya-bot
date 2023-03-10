from typing import List
from pathlib import Path

from aiogram import types

from .chat_history import get_text_from_txt, CHAT_HISTORY_PATH
from .markov import generate_sentence


# SHORT_MESSAGE_LENGTH = 100


def get_chat_history(chat_id: int) -> str:
    path = Path(CHAT_HISTORY_PATH) / f"{chat_id}.txt"
    if not path.exists():
        return
    text = get_text_from_txt(path)
    return text


async def generate_random_sentence(messages: List[str], chat_id: int) -> str:
    if not messages:
        return
    await types.ChatActions.typing()
    chat_history = get_chat_history(chat_id) or ""
    text = "\n".join(messages)
    sentence = generate_sentence(text + chat_history)
    return sentence.lower()
