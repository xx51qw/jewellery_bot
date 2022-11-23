from aiogram.utils import executor
from loguru import logger
from commands import set_default_commands
from handlers import dp


logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="1 week",
           compression="zip")


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)