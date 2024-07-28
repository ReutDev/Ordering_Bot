from aiogram import Bot  # Импорт класса Bot из aiogram для работы с ботом
from aiogram.types import BotCommand  # Импорт класса BotCommand для создания команд бота

from lexicon.lexicon import LEXICON_COMMANDS  # Импорт словаря команд из модуля lexicon


# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot):
    # Создание списка команд для главного меню
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS.items()  # Заполнение списка команд из словаря LEXICON_COMMANDS
    ]
    await bot.set_my_commands(main_menu_commands)  # Установка команд для бота
