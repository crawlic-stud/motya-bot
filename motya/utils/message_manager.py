from typing import List
from pathlib import Path
import json

from aiogram import types
from markovify import Text

from .chat_history import get_text_from_txt, CHAT_HISTORY_PATH
from .markov import generate_sentence
from data.anekdots import combine_all_anekdots


def _create_anekdot_model():
    print("fetching anekdots...")
    path = combine_all_anekdots()
    text = path.read_text(encoding="utf-8")
    print("creating model...")
    model = Text(text, well_formed=False)
    model = model.to_dict()
    model_path = Path.cwd() / "motya" / "data" / "models" / "anekdots.json"
    with open(model_path, "w", encoding="utf-8") as f:
        json.dump(model, f, indent=4)


# ANEKDOT_TEXT_MODEL = _create_anekdot_model()


def _get_chat_history(chat_id: int) -> str:
    path = Path(CHAT_HISTORY_PATH) / f"{chat_id}.txt"
    if not path.exists():
        return
    text = get_text_from_txt(path)
    return text


async def _get_text(messages: List[str]) -> str:
    if not messages:
        return
    await types.ChatActions.typing()
    text = "\n".join(messages)
    return text


async def random_sentence_from_messages(messages: List[str]) -> str:
    text = await _get_text(messages)
    sentence = generate_sentence(text)
    return sentence.lower()


async def random_sentence(messages: List[str], chat_id: int) -> str:
    chat_history = _get_chat_history(chat_id) or ""
    text = await _get_text(messages)
    sentence = generate_sentence(text + chat_history)
    return sentence.lower()


async def anekdot():
    await types.ChatActions.typing()
    sentence = ANEKDOT_TEXT_MODEL.make_sentence(tries=100)
    return sentence.lower()