from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from parse import scrap_contacts
from loguru import logger


@logger.catch
@dp.message_handler(Command('contacts'))
async def help_info(message: types.Message) -> None:
    contacts = await scrap_contacts()
    phone = contacts[0]
    email = contacts[1]
    email2 = contacts[2]
    location = contacts[3]
    await message.answer(f'\n&#128222; {phone}\n&#128231; {email}\n&#128231; {email2}\n&#128205; {location}'
                         f'\n Парковка на крыше ТЦ Сфера', parse_mode='html')
    await message.answer_location(latitude=55.753049716753985, longitude=37.57604176786673, horizontal_accuracy=0)
