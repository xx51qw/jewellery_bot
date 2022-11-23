from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageToDeleteNotFound
from loader import dp
from loguru import logger
import time

from parse import scrap_links, all_items
from states import Category
from keyboard import collection_keyboard, type_jewellery_keyboard


@logger.catch
@dp.message_handler(Command('catalog'))
async def choose_collection(message: Message) -> None:
    """Хендлер для выбора ювелирной коллекции"""
    keyboard = await collection_keyboard()
    await message.answer('Выберите коллекцию:', reply_markup=keyboard)
    await Category.collection.set()


@logger.catch
@dp.callback_query_handler(state=Category.collection)
async def choose_type_jewellery(callback: CallbackQuery, state: FSMContext) -> None:
    """Хендлер для выбора категории украшений"""
    if callback.data == 'stop':
        await state.reset_state()
        await callback.message.delete()
        await callback.message.answer('Выберите команду: '
                                      '\n/start - Запустить бота 💻'
                                      '\n/help - Помощь 📣'
                                      '\n/catalog - Каталог ювелирных изделий 📖'
                                      '\n/about - Информация о нас ℹ️'
                                      '\n/delivery - Оплата и доставка 💵'
                                      '\n/contacts", "Контакты и адрес Ювелирного дома 📞;'
                                      )

    else:
        await state.update_data(collection=callback.data)
        await callback.message.delete()
        data = await state.get_data()
        collection = data['collection']
        keyboard = await type_jewellery_keyboard(collection)
        await callback.message.answer('Выберите тип украшения:', reply_markup=keyboard)
        await Category.jewellery.set()


@logger.catch
@dp.callback_query_handler(state=Category.jewellery)
async def choose_type_jewellery(callback: CallbackQuery, state: FSMContext) -> None:
    """Хендлер для получения информации о ювелирном изделии"""
    await callback.message.delete()
    if callback.data == 'back':
        try:
            keyboard = await collection_keyboard()
            await callback.message.answer('Выберите коллекцию:', reply_markup=keyboard)
            await Category.collection.set()
        except MessageToDeleteNotFound as ex:
            logger.exception(ex)

    else:
        await state.update_data(jewellery=callback.data)
        data = await state.get_data()
        jewellery = data.get('jewellery')
        links = await scrap_links(jewellery)
        product_list = await all_items(links)
        if product_list:
            for product in product_list:
                if product:
                    img = product.get('img')
                    title = product.get('title')
                    price = product.get('price')
                    availability = product.get('availability')
                    description = product.get('description')
                    url = product.get('url')
                    await callback.message.bot.send_photo(photo=img, caption=f'{title} \n{price} \n{availability} \n'
                                                                             f'{description} \n{url}',
                                                          chat_id=callback.message.chat.id)
                    time.sleep(0.3)
        else:
            await callback.message.answer('В указанную категорию украшения еще не добавили')

        await state.reset_state()
