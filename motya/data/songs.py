import asyncio
from ctypes.wintypes import LPBYTE
from typing import AsyncIterator

import aiohttp
from pydantic import BaseModel
from bs4 import BeautifulSoup


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
    sections = data["response"]["sections"]

    result = {}
    for section in sections:
        if section["type"] == "artist":
            result = section["hits"][0]["result"]
            break

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


async def main():
    artist = await get_artist_data("noize mc")
    if artist is not None:
        songs = await get_artist_songs(artist.api_path)
        lyrics = []
        async for song in get_song_lyrics(songs):
            lyrics.append(song)
            print(song.lyrics)
    return


if __name__ == "__main__":
    asyncio.run(main())
