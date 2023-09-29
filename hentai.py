import aiohttp
from random import choice
from typing import TypedDict, cast

ENDPOINT = "http://api.nekos.fun:8080/api/%s"

TAGS = ["tag", "kiss", "lick", "hug", "baka", "cry", "poke", "smug", "slap", "tickle", "pat", "laugh", "feed", "cuddle", "tag",
        "4k", "ass", "blowjob/bj", "boobs", "cum", "feet", "hentai", "wallpapers", "spank", "gasm", "lesbian", "lewd", "pussy"]


class _Response(TypedDict):
    image: str


async def get_random_image() -> str:
    tag = choice(TAGS)
    async with aiohttp.ClientSession() as session:
        async with session.get(ENDPOINT % tag) as response:
            data = cast(_Response, await response.json())
            return data['image']
