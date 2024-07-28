import logging

from aiogram import Router
from aiogram.types import Message

from database.database import CHANGED  # Импорт переменной CHANGED из модуля database.database
from lexicon.lexicon import LEXICON  # Импорт словаря LEXICON из модуля lexicon.lexicon

router = Router()  # Инициализация роутера для обработки сообщений
logger = logging.getLogger(__name__)  # Получение логгера для текущего модуля

# Настройка логирования
logging.basicConfig(level=logging.INFO)  # Установка уровня логирования INFO
formatter = logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
file_handler = logging.FileHandler('bot_logs.log', mode='a', encoding='utf-8')  # Создание файла для логов
file_handler.setFormatter(formatter)  # Установка форматтера для файла логов
logger.addHandler(file_handler)  # Добавление файла логов к логгеру


# Обработчик для всех остальных сообщений
@router.message()
async def other(message: Message):
    user_id = message.from_user.id  # Получаем ID пользователя
    await message.delete()  # Удаляем полученное сообщение
    msg = await message.answer(LEXICON['error'])  # Отправляем пользователю сообщение об ошибке из словаря LEXICON
    CHANGED[user_id].append(msg)  # Добавляем сообщение в список изменений для данного пользователя
