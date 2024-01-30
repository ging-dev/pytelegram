import os
import re
import aiohttp
from lxml import html
from lxml.html import HtmlElement
from aiogram import Bot, Dispatcher, executor, types
from api import reply_from_openai
from hentai import get_random_image

bot = Bot(token=os.environ['BOT_TOKEN'])
dp = Dispatcher(bot)
qa_prefix = 'qa:'


@dp.message_handler()
async def on_callback(message: types.Message) -> None:
    text = message.text.encode('ascii', 'ignore').decode()

    if message.text.startswith(qa_prefix):
        question = text.lstrip(qa_prefix).strip()
        message = await message.reply('Chờ tí tao tra Google...')
        await message.edit_text(
            await reply_from_openai(question, message.from_user.id),
            parse_mode=types.ParseMode.MARKDOWN
        )

    if message.text.lower() == "!hentai":
        image_url = await get_random_image()
        await (message.answer_animation
               if image_url.endswith('.gif')
               else message.answer_photo)(image_url)

    matches = re.match(r'(https://\S+)', text)

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
