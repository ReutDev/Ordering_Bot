import os

from services.file_handling import json_to_dict

# Загружаем данные из JSON файла и нормализуем путь для корректного отображения
data = json_to_dict(os.path.normpath(r'C:\Users\Asus\PycharmProjects\Ordering_Bot\media_id.json'))

# Формируем словари для категорий, подкатегорий и предметов на основе данных JSON
LEXICON_CAT: list[str] = list(data.keys())  # Список категорий
LEXICON_SUBCAT: list[list[str]] = [list(sub.keys()) for sub in data.values()]  # Список подкатегорий
LEXICON_ITEM: list[list[list[str]]] = [[paintings for paintings in sub.values()] for sub in
                                       data.values()]  # Список картин

# ID фото для превью
PREVIEW = "AgACAgIAAxkBAAPPZpgZn_QFXQypa38LzpL5hXmv0hYAArThMRubdMBI82MPVraUCQgBAAMCAAN5AAM1BA"

# Инициализируем "базу данных" пользователей
USERS: dict[int, dict[str, int]] = {}

# Инициализируем "базу данных" для отслеживания изменений сообщений при команде /reset
CHANGED: dict[int, list] = {}
