import os
import re
import aiohttp
from lxml import html
from lxml.html import HtmlElement
from aiogram import Bot, Dispatcher, executor, types
from api import reply_from_openai
from hentai import get_random_image

bot = Bot(token="6308559113:AAH7C-UDiYNA3kivaG9uBI2Vgw0YWDkqp1Y")
dp = Dispatcher(bot)
qa_prefix = 'qa:'

@dp.message_handler()
async def on_callback(message: types.Message) -> None:
    # m đố đố cc
    if "đố mn" in message.text.lower():
        await message.reply('đố đố cc')

    if message.text.startswith(qa_prefix):
        question = message.text.lstrip(qa_prefix).strip()
        message = await message.reply('Chờ tí tao tra Google...')
        await message.edit_text(
            await reply_from_openai(question, message.from_user.id),
            parse_mode=types.ParseMode.MARKDOWN
        )

    matches = re.match(r'(https://\S+)', message.text.encode('ascii', 'ignore').decode())

    if len(message.text) < 2 and message.text != 'ê':
        await message.reply('ai phụ huynh bé ton đón cháu về nè')
    if message.text == 'ê':
        await message.reply('j')
    if message.text.lower() == "!hentai":
        image_url = await get_random_image()
        await message.answer_photo(photo=image_url)

    if not matches:
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(matches[0]) as response:
            dom: HtmlElement = html.fromstring(await response.text())
            if not dom.xpath('//meta[@name="tt_category_id" and @content="1001014"]'):
                return

    await message.reply('Hành vi của bạn vi phạm tiêu chuẩn cộng đồng của nhóm.')
    await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)