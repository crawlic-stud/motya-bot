import asyncio
from typing import AsyncIterator

import aiohttp
from pydantic import BaseModel
from bs4 import BeautifulSoup

from config import songs_db


BASE_URL = "https://genius.com/api"


class Artist(BaseModel):
    api_path: str
    image_url: str
    url: str
    name: str


class Song(BaseModel):
    api_path: str
    full_title: str
    url: str


class SongWithLyrics(BaseModel):
    song_id: str
    lyrics: str


async def get_artist_data(artist: str) -> Artist | None:
    url = f"{BASE_URL}/search/multi?q={artist}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if not response.ok:
                return
            data = await response.json(encoding="utf-8")
    result = {}
    try:
        sections = data["response"]["sections"]
        for section in sections:
            if section["type"] == "artist":
                result = section["hits"][0]["result"]
                break
    except (IndexError, KeyError):
        return

    return Artist(**result)


async def timeout():
    await asyncio.sleep(0.05)


async def get_artist_songs(artist_api_path: str) -> list[Song]:
    url = (
        BASE_URL
        + artist_api_path
        + "/songs?page={page}&per_page=20&sort=popularity&text_format=html%2Cmarkdown"
    )
    songs = []
    max_recursion = 100
    async with aiohttp.ClientSession() as session:
        for i in range(max_recursion):
            async with session.get(url.format(page=i + 1)) as response:
                await timeout()
                if not response.ok:
                    continue
                data = await response.json(encoding="utf-8")
                songs_data = data.get("response", {}).get("songs", [])
                if not songs_data:
                    break
                for song in songs_data:
                    songs.append(Song(**song))
    return songs


def parse_lyrics_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    lyrics_element = soup.select_one("div[class^='Lyrics__Container']")
    if lyrics_element is None:
        return ""
    lyrics = []
    for content in lyrics_element.contents:
        if isinstance(content, str) and not content.startswith("["):
            lyrics.append(content)
    return "\n".join(lyrics)


async def get_song_lyrics(songs: list[Song]) -> AsyncIterator[SongWithLyrics]:
    async with aiohttp.ClientSession() as session:
        for song in songs:
            await timeout()
            async with session.get(song.url) as response:
                html = await response.text(encoding="utf-8")
                parsed_lyrics = parse_lyrics_html(html)
                song_id = song.url.split("/")[-1]
                yield SongWithLyrics(song_id=song_id, lyrics=parsed_lyrics)


async def get_existing_songs(artist_name: str) -> tuple[Artist | None, list[str]]:
    if not artist_name:
        return None, songs_db.get_all_songs()
    artist = await get_artist_data(artist_name)
    existing_songs = []
    if artist is not None:
        existing_songs = songs_db.get_songs(artist.api_path)
    return artist, existing_songs


async def get_songs_and_save_to_db(artist: Artist | None) -> list[str]:
    lyrics = []
    if artist is not None:
        songs = await get_artist_songs(artist.api_path)
        async for song in get_song_lyrics(songs):
            lyrics.append(song.lyrics)
        songs_db.add_songs(artist.api_path, lyrics)
    return lyrics


async def main():
    artist, songs = await get_existing_songs("noize mc")
    if not songs:
        songs = await get_songs_and_save_to_db(artist)
    for song in songs:
        print(song)


if __name__ == "__main__":
    asyncio.run(main())
