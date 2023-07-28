import os
import re
import aiohttp
from lxml import html
from lxml.html import HtmlElement
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(bot)

@dp.message_handler()
async def on_callback(message: types.Message) -> None:
    links = re.match(r'(https://\S+)', message.text)

    if not links:
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(links[0]) as response:
            dom: HtmlElement = html.fromstring(await response.text())
            tam_su: list = dom.xpath('//meta[@name="tt_category_id" and @content="1001014"]')
            if not tam_su:
                return

    await message.answer('Fuk vnexpress !!!')
    await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
