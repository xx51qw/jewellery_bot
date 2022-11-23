from loguru import logger
from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from parse import scrap_about


@logger.catch
@dp.message_handler(Command('about'))
async def help_info(message: types.Message) -> None:
    info = await scrap_about()
    text = ''
    for i in info:
        text += i + '\n'
    text += 'https://danielmalaev.ru'
    await message.answer(text,disable_web_page_preview=True)
