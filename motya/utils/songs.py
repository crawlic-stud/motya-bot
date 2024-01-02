from aiogram import types

from .tools import words_after
from data.songs import get_existing_songs, get_songs_and_save_to_db


downloading_songs = set()


async def get_songs(message: types.Message, command: str):
    msg_text = message.text if message.text else ""
    artist_name = words_after(msg_text, command)
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
