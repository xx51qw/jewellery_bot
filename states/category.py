from aiogram.dispatcher.filters.state import StatesGroup, State


class Category(StatesGroup):
    collection = State()
    jewellery = State()