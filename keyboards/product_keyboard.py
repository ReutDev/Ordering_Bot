from aiogram.types import InlineKeyboardButton, \
    InlineKeyboardMarkup  # Импорт классов для создания inline-кнопок и разметки

from lexicon.lexicon import LEXICON  # Импорт словаря LEXICON для текста кнопок
from services.file_handling import GoodsCallbackFactory  # Импорт фабрики колбэков для обработки нажатий кнопок


# Функция для создания клавиатуры категорий
def create_category_keyboard(categories):
    buttons = []
    for idx, category in enumerate(categories):
        buttons.append([InlineKeyboardButton(
            text=category,
            callback_data=GoodsCallbackFactory(category_id=idx, subcategory_id=-1, item_id=-1).pack()
        )])  # Создание кнопок для каждой категории с колбэком
    return InlineKeyboardMarkup(inline_keyboard=buttons)  # Возврат разметки с кнопками


# Функция для создания клавиатуры подкатегорий
def create_subcategory_keyboard(category_idx, subcategories):
    buttons = []
    for idx, subcategory in enumerate(subcategories[category_idx]):
        buttons.append([InlineKeyboardButton(
            text=subcategory,
            callback_data=GoodsCallbackFactory(category_id=category_idx, subcategory_id=idx, item_id=-1).pack()
        )])  # Создание кнопок для каждой подкатегории с колбэком
    buttons.append([InlineKeyboardButton(text="Назад", callback_data=LEXICON['back'])])  # Добавление кнопки "Назад"
    return InlineKeyboardMarkup(inline_keyboard=buttons)  # Возврат разметки с кнопками


# Функция для создания клавиатуры товаров
def create_item_keyboard(category_idx, subcategory_idx, items):
    buttons = []
    for idx, item in enumerate(items[category_idx][subcategory_idx]):
        buttons.append([InlineKeyboardButton(
            text=f"Картина {idx + 1}",
            callback_data=GoodsCallbackFactory(category_id=category_idx, subcategory_id=subcategory_idx,
                                               item_id=idx).pack()
        )])  # Создание кнопок для каждого товара с колбэком
    buttons.append([InlineKeyboardButton(text="Назад", callback_data=LEXICON['back'])])  # Добавление кнопки "Назад"
    return InlineKeyboardMarkup(inline_keyboard=buttons)  # Возврат разметки с кнопками


# Функция для создания клавиатуры оплаты
def create_pay_keyboard():
    buttons = []
    buttons.extend([
        [InlineKeyboardButton(text='Контакты для заказа', url='https://t.me/and_reut')],
        [InlineKeyboardButton(text=LEXICON['reset'], callback_data=LEXICON['reset'])],
        [InlineKeyboardButton(text=LEXICON['pay'], callback_data=LEXICON['pay'])]
    ])  # Создание кнопок для контактов, сброса и оплаты
    return InlineKeyboardMarkup(inline_keyboard=buttons)  # Возврат разметки с кнопками


# Словарь, связывающий уровни меню с соответствующими функциями создания клавиатур
dict_reply = {
    0: create_category_keyboard,
    1: create_subcategory_keyboard,
    2: create_item_keyboard,
    3: create_pay_keyboard
}
