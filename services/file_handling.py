import json
import logging

from aiogram.filters import BaseFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ContentType

logger = logging.getLogger(__name__)


class IsAdmin(BaseFilter):
    def __init__(self, admin_ids):
        self.admin_ids = admin_ids

    async def __call__(self, message: Message):
        return message.from_user.id in self.admin_ids


def write_id_json(message: Message):
    message_type = message.content_type
    try:
        if message_type != ContentType.PHOTO:
            logger.info('Не поддерживаемый тип файла')
            return None
    except Exception as e:
        logger.exception(f'{message_type} не имеет ID, ошибка типа {e}', exc_info=True)
        return None

    try:
        with open('media_id.json', 'r', encoding='utf-8') as file:
            buf_dict = json.load(file)
    except FileNotFoundError:
        buf_dict = {}

    try:
        caption = message.caption.lower()
        parts = caption.split()
        cat, sub_cat = parts[0].capitalize(), ' '.join(parts[1:]).capitalize()
    except AttributeError as e:
        logger.exception(f"Ошибка обработки подписи: {e}", exc_info=True)
        return None

    id_obj, uniq_id = message.photo[-1].file_id, message.photo[-1].file_unique_id
    buf_dict.setdefault(cat, {}).setdefault(sub_cat, [])

    if not any(uniq_id in photo for photo in buf_dict[cat][sub_cat]):
        buf_dict[cat][sub_cat].append([id_obj, uniq_id])
        logger.info(f'Фото добавлено с id={id_obj} в категорию: {cat}, подкатегорию: {sub_cat}')
    else:
        logger.info(f'id={id_obj} уже существует в категории: {cat}, подкатегории: {sub_cat}')
        return None

    try:
        with open('media_id.json', 'w', encoding='utf-8') as file:
            json.dump(buf_dict, file, ensure_ascii=False, indent=4)
            return True
    except IOError as e:
        logger.exception(f"Ошибка записи в файл: {e}", exc_info=True)
        return None


def json_to_dict(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


class GoodsCallbackFactory(CallbackData, prefix='goods', sep='|'):
    category_id: int
    subcategory_id: int
    item_id: int
