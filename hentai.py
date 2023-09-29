from random import choice
import aiohttp
import json
endpoint = "http://api.nekos.fun:8080/api/%s"
tags = ["tag", "kiss", "lick", "hug", "baka", "cry", "poke", "smug", "slap", "tickle", "pat", "laugh", "feed", "cuddle", "tag", "4k", "ass", "blowjob/bj", "boobs", "cum", "feet", "hentai", "wallpapers", "spank", "gasm", "lesbian", "lewd", "pussy"]
async def get_random_image() -> str:
    tag = choice(tags)
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint % tag) as response:
            data = await response.json()
            return data["image"]