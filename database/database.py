import os

from services.file_handling import json_to_dict

data = json_to_dict(os.path.normpath(r'C:\Users\Asus\PycharmProjects\TelegramBot\Maryam\media_id.json'))

LEXICON_CAT: list[str] = list(data.keys())
LEXICON_SUBCAT: list[list[str]] = [list(sub.keys()) for sub in data.values()]
LEXICON_ITEM: list[list[list[str]]] = [[paintings for paintings in sub.values()] for sub in data.values()]
PREVIEW = "AgACAgIAAxkBAAPPZpgZn_QFXQypa38LzpL5hXmv0hYAArThMRubdMBI82MPVraUCQgBAAMCAAN5AAM1BA"
# Создаем шаблон заполнения словаря с выборами пользователей
user_dict_template: dict[str: int] = {
    'level': 0,
    'cat': 0,
    'sub_cat': 0,
    'item': 0,
    'payment': 0,
    'start': 0
}

# Инициализируем "базу данных" пользователей
USERS: dict[int: dict[str: int]] = {}

# Инициализируем "базу данных" сообщений для сброса при коменде /reset
CHANGED: dict[int: list] = {}
