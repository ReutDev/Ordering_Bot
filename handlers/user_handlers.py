import logging

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message, InputMediaPhoto

from database.database import LEXICON_CAT, LEXICON_ITEM, LEXICON_SUBCAT, PREVIEW, CHANGED
from keyboards.product_keyboard import dict_reply
from lexicon.lexicon import LEXICON
from services.file_handling import GoodsCallbackFactory, save_users, load_users, update_user

# Создание роутера для обработки сообщений и колбеков
router = Router()

# Настройка логирования
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s '
                              '[%(asctime)s] - %(name)s - %(message)s')
file_handler = logging.FileHandler('bot_logs.log', mode='a', encoding='utf-8')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if str(user_id) not in load_users():  # Проверка, есть ли пользователь в базе
        update_user(user_id, {  # Сброс данных пользователя
            'level': 0,
            'cat': 0,
            'sub_cat': 0,
            'item': 0,
            'start': 0
        })
    if not load_users()[str(user_id)]['start']:  # Если это первый запуск для пользователя
        update_user(user_id, {'level': 0})  # Обновление уровня пользователя
        msg = await message.answer_photo(photo=PREVIEW,
                                         caption=f'Привет, {message.from_user.first_name}\n{LEXICON["/start"]}{LEXICON["cat"]}',
                                         reply_markup=dict_reply[load_users()[str(user_id)]['level']](LEXICON_CAT)
                                         )
        if user_id not in CHANGED:  # Инициализация списка изменений для пользователя
            CHANGED[user_id] = []
        CHANGED[user_id].append(msg)  # Добавление сообщения в список изменений
        update_user(user_id, {'start': 1})  # Обновление состояния пользователя
    else:
        msg = await message.answer(text=LEXICON['error'])  # Ошибка при повторном запуске
        CHANGED[user_id].append(msg)


# Обработчик команды /help
@router.message(Command(commands=['help']))
async def cmd_help(message: Message):
    msg = await message.answer(text=LEXICON['/help'])
    user_id = message.from_user.id
    if user_id in CHANGED:  # Проверка, есть ли изменения для пользователя
        CHANGED[user_id].append(msg)


# Обработчик команды /contacts
@router.message(Command(commands=['contacts']))
async def cmd_contacts(message: Message):
    msg = await message.answer(text=LEXICON['/contacts'])
    user_id = message.from_user.id
    if user_id in CHANGED:
        CHANGED[user_id].append(msg)
    logger.info(f'Пользователь: tg://user?id={message.from_user.id} запросил контакты')  # Логирование запроса контактов


# Обработчик команды /reset
@router.message(Command(commands=['reset']))
async def cmd_reset(message: Message):
    user_id = message.from_user.id
    update_user(user_id, {  # Сброс данных пользователя
        'level': 0,
        'cat': 0,
        'sub_cat': 0,
        'item': 0,
        'start': 0
    })
    logger.info(f'Пользователь: tg://user?id={message.from_user.id} сбросил бота')  # Логирование сброса
    await message.answer(text=LEXICON['/reset'])
    if user_id in CHANGED:
        for msg in CHANGED[user_id]:
            try:
                if not isinstance(msg, list):
                    await msg.delete()  # Удаление сообщения
                else:
                    for ms in msg:
                        await ms.delete()
            except TelegramBadRequest:
                pass  # Игнорирование ошибок при удалении
        CHANGED[user_id] = []  # Очистка списка изменений


# Обработчик колбека для сброса
@router.callback_query(F.data == LEXICON['reset'])
async def process_reset(callback: CallbackQuery):
    user_id = callback.from_user.id
    update_user(user_id, {'level': 0})  # Сброс уровня пользователя
    await callback.message.delete()  # Удаление сообщения
    msg = await callback.message.answer_photo(photo=PREVIEW,
                                              caption=f'Привет, {callback.from_user.first_name}\n{LEXICON["/start"]}{LEXICON["cat"]}',
                                              reply_markup=dict_reply[load_users()[str(user_id)]['level']](LEXICON_CAT)
                                              )
    if user_id in CHANGED:
        CHANGED[user_id].append(msg)  # Добавление сообщения в список изменений


# Обработчик колбека для оплаты
@router.callback_query(F.data == LEXICON['pay'])
async def process_pay(callback: CallbackQuery):
    await callback.message.delete()  # Удаление сообщения
    await callback.answer(text=LEXICON['form'], show_alert=True)  # Отправка уведомления
    user_id = callback.from_user.id
    await callback.bot.send_photo(
        photo=LEXICON_ITEM[load_users()[str(user_id)]["cat"]][load_users()[str(user_id)]["sub_cat"]][
            load_users()[str(user_id)]["item"]][0],
        caption=f' От tg://user?id={callback.from_user.id} завершил заказ',
        chat_id=733076652)
    logger.info(f'Оформление заказа от пользователя tg://user?id={callback.from_user.id}')  # Логирование заказа
    await callback.bot.send_photo(
        chat_id=callback.from_user.id,
        photo=LEXICON_ITEM[load_users()[str(user_id)]["cat"]][load_users()[str(user_id)]['sub_cat']][
            load_users()[str(user_id)]['item']][0],
        caption=LEXICON['success']
    )
    update_user(user_id, {  # Сброс данных пользователя после заказа
        'level': 0,
        'cat': 0,
        'sub_cat': 0,
        'item': 0,
        'start': 0
    })


# Обработчик колбека для возврата на предыдущий уровень
@router.callback_query(F.data == LEXICON['back'])
async def process_back(callback: CallbackQuery):
    user_id = callback.from_user.id
    level = load_users()[str(user_id)]['level'] - 1
    update_user(user_id, {'level': level})  # Обновление уровня пользователя
    if level == 0:
        msg = await callback.message.edit_media(media=InputMediaPhoto(media=PREVIEW,
                                                                      caption=f'Привет, {callback.from_user.first_name}\n{LEXICON["/start"]}{LEXICON["cat"]}'),
                                                reply_markup=dict_reply[load_users()[str(user_id)]['level']](
                                                    LEXICON_CAT))
        if user_id not in CHANGED:
            CHANGED[user_id] = []
        CHANGED[user_id].append(msg)  # Добавление сообщения в список изменений

    elif level == 1:
        await callback.message.delete()
        msg = await callback.message.answer_photo(photo=PREVIEW,
                                                  caption=f'Вы выбрали категорию: {LEXICON_CAT[load_users()[str(user_id)]["cat"]]}\n\nВыберите подкатегорию:',
                                                  reply_markup=dict_reply[level](load_users()[str(user_id)]['cat'],
                                                                                 LEXICON_SUBCAT))
        if user_id in CHANGED:
            CHANGED[user_id].append(msg)  # Добавление сообщения в список изменений
    elif level == 2:
        msg = await callback.message.edit_text(
            text=LEXICON['item_id'],
            reply_markup=dict_reply[level](load_users()[str(user_id)]['cat'], load_users()[str(user_id)]['sub_cat'],
                                           LEXICON_ITEM))
        if user_id not in CHANGED:
            CHANGED[user_id] = []
        CHANGED[user_id].append(msg)  # Добавление сообщения в список изменений


# Обработчик колбека для выбора товара
@router.callback_query(GoodsCallbackFactory.filter())
async def process_press(callback: CallbackQuery, callback_data: GoodsCallbackFactory):
    user_id = str(callback.from_user.id)  # Используйте строковое представление user_id для работы с JSON
    users = load_users()
    users[user_id]['level'] += 1  # Повышение уровня пользователя
    save_users(users)
    level = users[user_id]['level']

    if level == 1:
        user_id = callback.from_user.id
        update_user(user_id, {'cat': int(callback_data.category_id)})  # Обновление категории пользователя
        msg = await callback.bot.edit_message_media(chat_id=callback.message.chat.id,
                                                    message_id=callback.message.message_id,
                                                    media=InputMediaPhoto(media=PREVIEW,
                                                                          caption=f'Вы выбрали категорию: {LEXICON_CAT[load_users()[str(user_id)]["cat"]]}'
                                                                                  f'\n\nВыберите подкатегорию:'),
                                                    reply_markup=dict_reply[level](load_users()[str(user_id)]['cat'],
                                                                                   LEXICON_SUBCAT))
        if user_id not in CHANGED:
            CHANGED[user_id] = []
        CHANGED[user_id].append(msg)
    elif level == 2:
        user_id = callback.from_user.id
        update_user(user_id, {'sub_cat': int(callback_data.subcategory_id)})
        media = [
                    InputMediaPhoto(
                        media=LEXICON_ITEM[load_users()[str(user_id)]['cat']][load_users()[str(user_id)]['sub_cat']][0][
                            0],
                        caption=f'Вы выбрали категорию: {LEXICON_CAT[load_users()[str(user_id)]["cat"]]}\n'
                                f'Подкатегорию: {LEXICON_SUBCAT[load_users()[str(user_id)]['cat']][load_users()[str(user_id)]['sub_cat']]}')
                ] + [
                    InputMediaPhoto(
                        media=LEXICON_ITEM[load_users()[str(user_id)]['cat']][load_users()[str(user_id)]['sub_cat']][i][
                            0]
                    ) for i in range(1, len(
                LEXICON_ITEM[load_users()[str(user_id)]['cat']][load_users()[str(user_id)]['sub_cat']]))
                ]
        await callback.message.delete()
        msg = await callback.message.answer_media_group(media=media)
        if user_id not in CHANGED:
            CHANGED[user_id] = []
        CHANGED[user_id].append(msg)
        msg = await callback.message.answer(
            text=LEXICON['change'],
            reply_markup=dict_reply[level](load_users()[str(user_id)]['cat'], load_users()[str(user_id)]['sub_cat'],
                                           LEXICON_ITEM))
        CHANGED[user_id].append(msg)
    else:
        user_id = callback.from_user.id
        users = load_users()
        update_user(user_id, {'level': 3, 'item': int(callback_data.item_id)})

        await callback.message.delete()
        msg = await callback.bot.send_photo(chat_id=callback.from_user.id,
                                            photo=
                                            LEXICON_ITEM[load_users()[str(user_id)]['cat']][
                                                load_users()[str(user_id)]['sub_cat']][
                                                load_users()[str(user_id)]['item']][0],
                                            caption=f'{LEXICON["pay_process"]}'
                                                    f'Из категории: {LEXICON_CAT[load_users()[str(user_id)]['cat']]}\n'
                                                    f'Подкатегории: {LEXICON_SUBCAT[load_users()[str(user_id)]['cat']][load_users()[str(user_id)]['sub_cat']]}',
                                            reply_markup=dict_reply[load_users()[str(user_id)]['level']]()
                                            )
        if user_id in CHANGED:
            CHANGED[user_id].append(msg)
        update_user(user_id, {'level': users[str(user_id)]['level']})
