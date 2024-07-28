from aiogram import Router, F  # Импорт класса Router и F для фильтрации сообщений
from aiogram.types import Message  # Импорт класса Message для работы с сообщениями

from config_data.config import load_config  # Импорт функции load_config для загрузки конфигурации
from services.file_handling import IsAdmin, write_id_json  # Импорт классов IsAdmin и функции write_id_json

router = Router()  # Инициализация роутера для обработки сообщений

config = load_config('.env')  # Загрузка конфигурации из файла .env


# Обработчик сообщений для добавления фотографий, доступ только для администраторов и только с фото
@router.message(IsAdmin(config.tg_bot.admin_ids), F.photo)
async def add_pictuers(message: Message):
    if write_id_json(message=message):  # Попытка записи ID сообщения в JSON
        await message.answer('Картина добавлена ✅')  # Ответ при успешном добавлении
    else:
        await message.answer('Ошибка добавления ❌')  # Ответ при ошибке добавления
