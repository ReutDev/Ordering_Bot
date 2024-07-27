import logging

from aiogram import Router, F
from aiogram.types import Message

from config_data.config import load_config
from services.file_handling import IsAdmin, write_id_json

router = Router()
logger = logging.getLogger(__name__)

config = load_config('.env')


@router.message(IsAdmin(config.tg_bot.admin_ids), F.photo)
async def add_pictuers(message: Message):
    if write_id_json(message=message):
        await message.answer('Картина добавлена ✅')
    else:
        await message.answer('Ошибка добавления ❌')
