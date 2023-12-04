from aiogram import types

from config import pastas_db, arguments_db, common_db, dp, motya
from filters.motya_command import MotyaCommand
from filters.reply import Reply
from data.songs import get_existing_songs, get_songs_and_save_to_db
from utils.markov import generate_sentence
from utils.tools import words_after
from utils.message_manager import (
    answer_with_kb,
    random_anekdot,
    random_sentence,
    random_sentence_from_messages,
    reply_with_kb,
)


downloading_songs = set()


@dp.message_handler(MotyaCommand(["анекдот", "анек"], strict=True))
async def send_anekdot(message: types.Message):
    anekdot = await random_anekdot(3)
    if not anekdot:
        anekdot = await random_anekdot(2)
    await reply_with_kb(message, anekdot) if anekdot else None


@dp.message_handler(MotyaCommand(["паста"], strict=True))
async def send_pasta(message: types.Message):
    pastas = pastas_db.get_pastas()
    sentence = await random_sentence_from_messages(pastas)
    if not sentence:
        await message.reply("не получилось...")
        return
    await reply_with_kb(message, sentence)


@dp.message_handler(MotyaCommand(["ссора", "время"]))
async def get_time_since_last_argument(message: types.Message):
    arg_time = arguments_db.get_days_since_last_argument(message.chat.id)
    await message.reply(f"с прошлой ссоры прошло {arg_time}")


async def get_songs(message: types.Message, command: str):
    artist_name = words_after(message.text, command)
    artist, songs = await get_existing_songs(artist_name)
    if not artist:
        await message.reply("не нашел такого артиста...")
        return
    artist_id = artist.api_path
    if artist_id in downloading_songs:
        await message.reply("все еще читаю, ожидайте!!!")
        return
    # return
    if not songs:
        downloading_songs.add(artist_id)
        msg = await message.reply(f"читаю песни {artist.name}, ожидайте!")
        songs = await get_songs_and_save_to_db(artist)
        await msg.delete()
        downloading_songs.remove(artist_id)
    return songs


@dp.message_handler(MotyaCommand(["строчка"]))
async def get_line_for_artist(message: types.Message):
    songs = await get_songs(message, "строчка")
    if songs:
        sentence = generate_sentence("".join(songs))
        await reply_with_kb(message, sentence)


@dp.message_handler(MotyaCommand(["песня"]))
async def get_song_for_artist(message: types.Message):
    songs = await get_songs(message, "песня")
    if songs:
        songs_text = "".join(songs)
        sentence = "\n".join(generate_sentence(songs_text) for _ in range(4))
        await reply_with_kb(message, sentence)


@dp.message_handler(MotyaCommand([""]))
async def send_random_message(message: types.Message):
    messages = common_db.get_messages_from_chat(message.chat.id)
    sentence = await random_sentence(messages, message.chat.id)
    if not sentence:
        return
    await answer_with_kb(message, sentence)


@dp.message_handler(Reply(bot=motya))
async def answer_more(message: types.Message):
    return await send_random_message(message)
