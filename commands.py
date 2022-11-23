from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота 💻"),
        types.BotCommand("help", "Помощь 📣"),
        types.BotCommand("catalog", "Каталог ювелирных изделий 📖"),
        types.BotCommand("about", "Информация о нас ℹ"),
        types.BotCommand("delivery", "Оплата и доставка 💵"),
        types.BotCommand("contacts", "Контакты и адрес Ювелирного дома 📞"),
    ])