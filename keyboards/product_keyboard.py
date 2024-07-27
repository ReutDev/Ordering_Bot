from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from lexicon.lexicon import LEXICON
from services.file_handling import GoodsCallbackFactory


def create_category_keyboard(categories):
    buttons = []
    for idx, category in enumerate(categories):
        buttons.append([InlineKeyboardButton(text=category,
                                             callback_data=GoodsCallbackFactory(category_id=idx, subcategory_id=-1,
                                                                                item_id=-1).pack())])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_subcategory_keyboard(category_idx, subcategories):
    buttons = []
    for idx, subcategory in enumerate(subcategories[category_idx]):
        buttons.append([InlineKeyboardButton(text=subcategory,
                                             callback_data=GoodsCallbackFactory(category_id=category_idx,
                                                                                subcategory_id=idx,
                                                                                item_id=-1).pack())])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data=LEXICON['back'])])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_item_keyboard(category_idx, subcategory_idx, items):
    buttons = []
    for idx, item in enumerate(items[category_idx][subcategory_idx]):
        buttons.append([InlineKeyboardButton(text=f"Картина {idx + 1}",
                                             callback_data=GoodsCallbackFactory(category_id=category_idx,
                                                                                subcategory_id=subcategory_idx,
                                                                                item_id=idx).pack())])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data=LEXICON['back'])])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def create_pay_keyboard():
    buttons4 = []
    buttons4.extend([[InlineKeyboardButton(text='Контакты для заказа', url='https://t.me/and_reut')],
                     [InlineKeyboardButton(text=LEXICON['reset'], callback_data=LEXICON['reset'])],
                     [InlineKeyboardButton(text=LEXICON['pay'], callback_data=LEXICON['pay'])]])
    markup = InlineKeyboardMarkup(inline_keyboard=buttons4)
    return markup


dict_reply = {0: create_category_keyboard,
              1: create_subcategory_keyboard,
              2: create_item_keyboard,
              3: create_pay_keyboard}
