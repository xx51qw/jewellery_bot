from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from loguru import logger


@logger.catch
@dp.message_handler(CommandStart())
async def help_info(message: types.Message) -> None:
    await message.answer('Чтобы узнать функционал бота, пропишите команду /help')

