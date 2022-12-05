#!/usr/bin/env python
# coding: utf-8
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from parse import scrap_collection, scrap_category


async def collection_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    collection = await scrap_collection()
    keyboard.add(InlineKeyboardButton(text=collection[0], callback_data='colleciy-svetlana-ermoleva'))
    keyboard.add(InlineKeyboardButton(text=collection[1], callback_data='colleciy-daniel-malaev'))
    keyboard.add(InlineKeyboardButton(text='Отмена', callback_data='stop'))

    return keyboard


async def type_jewellery_keyboard(collection):
    keyboard = InlineKeyboardMarkup(row_width=1)
    category = await scrap_category(collection)
    for title, href in category.items():
        keyboard.add(InlineKeyboardButton(text=title, callback_data=href))
    keyboard.add(InlineKeyboardButton(text='< Назад', callback_data='back'))

    return keyboard
