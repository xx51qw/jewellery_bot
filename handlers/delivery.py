from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from parse import scrap_delivery
from loguru import logger


@logger.catch
@dp.message_handler(Command('delivery'))
async def help_info(message: types.Message) -> None:
    info = await scrap_delivery()
    text = ''

    for item in info[1:]:
        text += str(item).replace('\n\n\n', '\n')
    await message.answer(text, parse_mode='html')
