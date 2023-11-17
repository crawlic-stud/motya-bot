import random
from pathlib import Path


from aiogram import types
from data.anekdots import ANEKDOTS_FOLDER
from markovify import Text

from .chat_history import CHAT_HISTORY_PATH, get_text_from_txt
from .markov import generate_sentence, generate_sentence_with_start


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


async def _get_text(messages: list[str]) -> str:
    if not messages:
        return ""
    await types.ChatActions.typing()
    text = "\n".join(messages)
    return text


async def random_sentence_from_messages(messages: list[str]) -> str:
    text = await _get_text(messages)
    sentence = generate_sentence(text)
    return sentence.lower()


async def random_sentence(messages: list[str], chat_id: int) -> str:
    chat_history = _get_chat_history(chat_id)
    text = await _get_text(messages)
    sentence = generate_sentence(text + chat_history)
    return sentence.lower()


async def random_sentence_with_start(
    starts: list[str], messages: list[str], chat_id: int
) -> str:
    chat_history = _get_chat_history(chat_id)
    text = await _get_text(messages)
    start = random.choice(starts)
    sentence = generate_sentence_with_start(text + chat_history, keyword=start)
    return sentence.lower()


async def random_anekdot(state_size=3) -> str:
    await types.ChatActions.typing()
    paths = _get_anekdots_paths()
    theme = random.choice(paths)
    model = Text(
        theme.read_text(encoding="utf-8"), well_formed=True, state_size=state_size
    )
    sentence = model.make_sentence(tries=1000) or ""
    return sentence.lower()
