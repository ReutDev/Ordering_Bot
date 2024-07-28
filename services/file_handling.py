import json
import logging

from aiogram.filters import BaseFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, ContentType

# Настройка логгирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s '
                              '[%(asctime)s] - %(name)s - %(message)s')
file_handler = logging.FileHandler('bot_logs.log', mode='a', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class IsAdmin(BaseFilter):
    """
    Фильтр для проверки, является ли пользователь администратором.

    Attributes:
        admin_ids (list): Список идентификаторов администраторов.
    """

    def __init__(self, admin_ids):
        self.admin_ids = admin_ids

    async def __call__(self, message: Message):
        """
        Проверяет, является ли отправитель сообщения администратором.

        Args:
            message (Message): Сообщение от пользователя.

        Returns:
            bool: True, если отправитель является администратором, иначе False.
        """
        return message.from_user.id in self.admin_ids


def write_id_json(message: Message):
    """
    Сохраняет идентификатор фотографии и категорию в JSON файл.

    Args:
        message (Message): Сообщение с фотографией.

    Returns:
        bool: True, если фотография успешно добавлена, иначе None.
    """
    message_type = message.content_type
    try:
        if message_type != ContentType.PHOTO:
            logger.info('Не поддерживаемый тип файла')
            return None
    except Exception as e:
        logger.exception(f'{message_type} не имеет ID, ошибка типа {e}', exc_info=True)
        return None

    try:
        # Открываем JSON файл для чтения текущих данных
        with open('media_id.json', 'r', encoding='utf-8') as file:
            buf_dict = json.load(file)
    except FileNotFoundError:
        # Если файл не найден, создаем пустой словарь
        buf_dict = {}

    try:
        # Обработка подписи сообщения для получения категории и подкатегории
        caption = message.caption.lower()
        parts = caption.split()
        cat, sub_cat = parts[0].capitalize(), ' '.join(parts[1:]).capitalize()
    except AttributeError as e:
        logger.exception(f"Ошибка обработки подписи: {e}", exc_info=True)
        return None

    id_obj, uniq_id = message.photo[-1].file_id, message.photo[-1].file_unique_id
    buf_dict.setdefault(cat, {}).setdefault(sub_cat, [])

    # Проверка уникальности фотографии
    if not any(uniq_id in photo for photo in buf_dict[cat][sub_cat]):
        buf_dict[cat][sub_cat].append([id_obj, uniq_id])
        logger.info(f'Фото добавлено с id={id_obj} в категорию: {cat}, подкатегорию: {sub_cat}')
    else:
        logger.info(f'id={id_obj} уже существует в категории: {cat}, подкатегории: {sub_cat}')
        return None

    try:
        # Сохраняем обновленный словарь в JSON файл
        with open('media_id.json', 'w', encoding='utf-8') as file:
            json.dump(buf_dict, file, ensure_ascii=False, indent=4)
            return True
    except IOError as e:
        logger.exception(f"Ошибка записи в файл: {e}", exc_info=True)
        return None


def json_to_dict(file_path):
    """
    Преобразует JSON файл в словарь.

    Args:
        file_path (str): Путь к JSON файлу.

    Returns:
        dict: Содержимое JSON файла в виде словаря.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# Файл для хранения данных пользователей
USERS_FILE = 'users.json'


def load_users():
    """
    Загружает данные пользователей из файла JSON.

    Если файл не существует или его содержимое не является допустимым JSON,
    возвращает пустой словарь.

    Returns:
        dict: Словарь с данными пользователей.
    """
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # Если файл не найден или содержит неверный JSON, возвращаем пустой словарь
        return {}


def save_users(users):
    """
    Сохраняет данные пользователей в файл JSON.

    Args:
        users (dict): Словарь с данными пользователей.
    """
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)


def update_user(user_id, updates):
    """
    Обновляет данные пользователя и сохраняет изменения в файл JSON.

    Args:
        user_id (int): Уникальный идентификатор пользователя.
        updates (dict): Словарь с обновляемыми значениями.
    """
    # Загружаем текущие данные пользователей
    users = load_users()
    user_id = str(user_id)  # Преобразовать user_id в строку для ключа словаря

    # Проверяем, существует ли пользователь, если нет - добавляем его
    if user_id not in users:
        users[user_id] = {
            'level': 0,
            'cat': 0,
            'sub_cat': 0,
            'item': 0,
            'start': 0
        }

    # Обновляем данные пользователя
    users[user_id].update(updates)

    # Сохраняем обновленный список пользователей в файл
    save_users(users)


class GoodsCallbackFactory(CallbackData, prefix='goods', sep='|'):
    """
    Фабрика для создания данных обратного вызова для товаров.

    Attributes:
        category_id (int): Идентификатор категории.
        subcategory_id (int): Идентификатор подкатегории.
        item_id (int): Идентификатор товара.
    """
    category_id: int
    subcategory_id: int
    item_id: int
