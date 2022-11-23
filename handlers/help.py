from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from loader import dp
from loguru import logger


@logger.catch
@dp.message_handler(CommandHelp())
async def help_info(message: types.Message) -> None:
    await message.answer('Список команд:'
                         '\n/start - Запустить бота 💻'
                         '\n/help - Помощь 📣'
                         '\n/catalog - Каталог ювелирных изделий 📖'
                         '\n/about - Информация о нас ℹ️'
                         '\n/delivery - Оплата и доставка 💵'
                         '\n/contacts", "Контакты и адрес Ювелирного дома 📞;'
                         )