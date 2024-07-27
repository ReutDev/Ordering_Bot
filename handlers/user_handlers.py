from copy import deepcopy

from aiogram import Router, F
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.filters.callback_data import CallbackQuery
from aiogram.types import Message, InputMediaPhoto

from database.database import LEXICON_CAT, LEXICON_ITEM, LEXICON_SUBCAT, PREVIEW, user_dict_template, USERS, \
    CHANGED
from keyboards.product_keyboard import dict_reply
from lexicon.lexicon import LEXICON
from services.file_handling import GoodsCallbackFactory

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    if user_id not in USERS:
        USERS[user_id] = deepcopy(user_dict_template)
    if not USERS[user_id]['start']:
        USERS[user_id]['level'] = 0
        msg = await message.answer_photo(photo=PREVIEW,
                                         caption=f'Привет, {message.from_user.first_name}\n{LEXICON["/start"]}{LEXICON["cat"]}',
                                         reply_markup=dict_reply[USERS[user_id]['level']](LEXICON_CAT)
                                         )
        if user_id not in CHANGED:
            CHANGED[user_id] = []
        CHANGED[user_id].append(msg)

        USERS[user_id]['start'] = 1
    else:
        msg = await message.answer(text=LEXICON['error'])
        CHANGED[user_id].append(msg)


@router.message(Command(commands=['help']))
async def cmd_help(message: Message):
    msg = await message.answer(text=LEXICON['/help'])
    user_id = message.from_user.id
    CHANGED[user_id].append(msg)


@router.message(Command(commands=['contacts']))
async def cmd_contacts(message: Message):
    msg = await message.answer(text=LEXICON['/contacts'])
    user_id = message.from_user.id
    CHANGED[user_id].append(msg)


@router.message(Command(commands=['reset']))
async def cmd_contacts(message: Message):
    user_id = message.from_user.id
    USERS[user_id]['start'] = 0
    await message.answer(text=LEXICON['/reset'])
    if user_id in CHANGED:
        for msg in CHANGED[user_id]:
            try:
                if not isinstance(msg, list):
                    await msg.delete()
                else:
                    for ms in msg:
                        await ms.delete()
            except TelegramBadRequest:
                pass


@router.callback_query(F.data == LEXICON['reset'])
async def process_reset(callback: CallbackQuery):
    user_id = callback.from_user.id
    USERS[user_id]['level'] = 0
    await callback.message.delete()
    msg = await callback.message.answer_photo(photo=PREVIEW,
                                              caption=f'Привет, {callback.from_user.first_name}\n{LEXICON["/start"]}{LEXICON["cat"]}',
                                              reply_markup=dict_reply[USERS[user_id]['level']](LEXICON_CAT)
                                              )
    user_id = callback.from_user.id
    CHANGED[user_id].append(msg)


@router.callback_query(F.data == LEXICON['pay'])
async def process_pay(callback: CallbackQuery):
    user_id = callback.from_user.id
    USERS[user_id]['payment'] = 1
    await callback.message.delete()
    msg = await callback.message.answer(text=LEXICON['adress'])
    await callback.answer(text=LEXICON['adress'], show_alert=True)
    user_id = callback.from_user.id
    CHANGED[user_id].append(msg)


@router.callback_query(F.data == LEXICON['back'])
async def process_back(callback: CallbackQuery):
    user_id = callback.from_user.id
    USERS[user_id]['level'] -= 1
    level = USERS[user_id]['level']
    if level == 0:
        msg = await callback.message.edit_media(media=InputMediaPhoto(media=PREVIEW,
                                                                      caption=f'Привет, {callback.from_user.first_name}\n{LEXICON["/start"]}{LEXICON["cat"]}'),
                                                reply_markup=dict_reply[USERS[user_id]['level']](LEXICON_CAT))
        user_id = callback.from_user.id
        CHANGED[user_id].append(msg)
    elif level == 1:
        await callback.message.delete()
        msg = await callback.message.answer_photo(photo=PREVIEW,
                                                  caption=f'Вы выбрали категорию: {LEXICON_CAT[USERS[user_id]["cat"]]}\n\nВыберите подкатегорию:',
                                                  reply_markup=dict_reply[level](USERS[user_id]['cat'], LEXICON_SUBCAT))
        user_id = callback.from_user.id
        CHANGED[user_id].append(msg)
    elif level == 2:
        msg = await callback.message.edit_text(
            text=LEXICON['item_id'],
            reply_markup=dict_reply[level](USERS[user_id]['cat'], USERS[user_id]['sub_cat'], LEXICON_ITEM))
        user_id = callback.from_user.id
        CHANGED[user_id].append(msg)


@router.callback_query(GoodsCallbackFactory.filter())
async def process_press(callback: CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    USERS[user_id]['level'] += 1
    level = USERS[user_id]['level']
    if level == 1:
        USERS[user_id]['cat'] = int(callback_data.category_id)
        msg = await callback.bot.edit_message_media(chat_id=callback.message.chat.id,
                                                    message_id=callback.message.message_id,
                                                    media=InputMediaPhoto(media=PREVIEW,
                                                                          caption=f'Вы выбрали категорию: {LEXICON_CAT[USERS[user_id]["cat"]]}'
                                                                                  f'\n\nВыберите подкатегорию:'),
                                                    reply_markup=dict_reply[level](USERS[user_id]['cat'],
                                                                                   LEXICON_SUBCAT))
        user_id = callback.from_user.id
        CHANGED[user_id].append(msg)
    elif level == 2:
        USERS[user_id]['sub_cat'] = int(callback_data.subcategory_id)
        media = [
                    InputMediaPhoto(
                        media=LEXICON_ITEM[USERS[user_id]['cat']][USERS[user_id]['sub_cat']][0][0],
                        caption=f'Вы выбрали категорию: {LEXICON_CAT[USERS[user_id]["cat"]]}\n'
                                f'Подкатегорию: {LEXICON_SUBCAT[USERS[user_id]["cat"]][USERS[user_id]["sub_cat"]]}')
                ] + [
                    InputMediaPhoto(
                        media=LEXICON_ITEM[USERS[user_id]['cat']][USERS[user_id]['sub_cat']][i][0]
                    ) for i in range(1, len(LEXICON_ITEM[USERS[user_id]['cat']][USERS[user_id]['sub_cat']]))
                ]
        await callback.message.delete()
        msg = await callback.message.answer_media_group(media=media)
        user_id = callback.from_user.id
        CHANGED[user_id].append(msg)
        msg = await callback.message.answer(
            text=LEXICON['change'],
            reply_markup=dict_reply[level](USERS[user_id]['cat'], USERS[user_id]['sub_cat'], LEXICON_ITEM))
        CHANGED[user_id].append(msg)
    else:
        USERS[user_id]['level'] = 3
        USERS[user_id]['item'] = int(callback_data.item_id)
        await callback.message.delete()
        msg = await callback.message.answer_photo(
            photo=LEXICON_ITEM[USERS[user_id]["cat"]][USERS[user_id]['sub_cat']][USERS[user_id]['item']][0],
            caption=f'{LEXICON["pay_process"]}'
                    f'Из категории: {LEXICON_CAT[USERS[user_id]["cat"]]}\n'
                    f'Подкатегории: {LEXICON_SUBCAT[USERS[user_id]["cat"]][USERS[user_id]["sub_cat"]]}',
            reply_markup=dict_reply[USERS[user_id]['level']]())
        CHANGED[user_id].append(msg)
        await callback.bot.send_photo(
            photo=LEXICON_ITEM[USERS[user_id]["cat"]][USERS[user_id]["sub_cat"]][USERS[user_id]["item"]][0],
            caption=f' От tg://user?id={callback.from_user.id} запрос заказа.',
            chat_id=733076652)
