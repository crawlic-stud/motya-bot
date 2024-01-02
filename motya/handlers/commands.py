from aiogram import types, Router

from config import pastas_db, arguments_db, common_db, motya
from filters.motya_command import MotyaCommand
from filters.reply import Reply
from utils.tools import words_after
from utils.markov import generate_sentence
from utils.songs import get_songs
from utils.image_generate import reply_with_image
from utils.message_manager import (
    answer_with_kb,
    random_anekdot,
    random_sentence,
    random_sentence_from_messages,
    reply_with_kb,
)


router = Router(name="commands")
downloading_songs = set()


@router.message(
    MotyaCommand(["нарисуй", "рисунок"], description="рисую на заказ", strict=True)
)
async def send_photo(message: types.Message):
    tmp = await message.reply("рисую, подожди немного друг")
    txt = message.text.lower() if message.text else ""
    prompt = words_after(txt, "мотя")
    await reply_with_image(message, prompt)
    await tmp.delete()


@router.message(
    MotyaCommand(["анекдот", "анек"], description="рассказываю анекдот", strict=True)
)
async def send_anekdot(message: types.Message):
    anekdot = await random_anekdot(3)
    if not anekdot:
        anekdot = await random_anekdot(2)
    await reply_with_kb(message, anekdot) if anekdot else None


@router.message(MotyaCommand(["паста"], description="пишу пасту с твича", strict=True))
async def send_pasta(message: types.Message):
    pastas = pastas_db.get_pastas()
    sentence = await random_sentence_from_messages(pastas, message.chat.id, bot=motya)
    if not sentence:
        await message.reply("не получилось...")
        return
    await reply_with_kb(message, sentence)


@router.message(
    MotyaCommand(["ссора", "время"], description="пишу время с последней ссоры")
)
async def get_time_since_last_argument(message: types.Message):
    arg_time = arguments_db.get_days_since_last_argument(message.chat.id)
    await message.reply(f"с прошлой ссоры прошло {arg_time}")


@router.message(
    MotyaCommand(
        ["строчка"],
        description="пишу строчку песни",
    )
)
async def get_line_for_artist(message: types.Message):
    songs = await get_songs(message, "строчка")
    if songs:
        sentence = generate_sentence("".join(songs))
        await reply_with_kb(message, sentence)


@router.message(
    MotyaCommand(
        ["песня"],
        description="пишу песенку",
    )
)
async def get_song_for_artist(message: types.Message):
    songs = await get_songs(message, "песня")
    if songs:
        songs_text = "".join(songs)
        sentence = "\n".join(generate_sentence(songs_text) for _ in range(4))
        await reply_with_kb(message, sentence)


@router.message(
    MotyaCommand(
        [""],
        description="пишу в чатик",
    )
)
async def send_random_message(message: types.Message):
    messages = common_db.get_messages_from_chat(message.chat.id)
    sentence = await random_sentence(messages, message.chat.id, bot=motya)
    if not sentence:
        return
    await answer_with_kb(message, sentence)


@router.message(Reply(bot=motya))
async def answer_more(message: types.Message):
    return await send_random_message(message)
