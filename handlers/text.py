from loguru import logger
from aiogram import types
from aiogram.dispatcher.filters import Text
from loader import dp
from parse import scrap_contacts


@logger.catch
@dp.message_handler(Text)
async def help_info(message: types.Message) -> None:
    phone = await scrap_contacts()
    await message.answer(f'По возникающим вопросам звоните по номеру: \n{phone[0]}')
