from aiogram import Bot, Dispatcher, types
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(config('TOKEN_BOT'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
