import logging

from aiogram import Router
from aiogram.types import Message

from database.database import LEXICON_ITEM, USERS, CHANGED
from lexicon.lexicon import LEXICON

router = Router()
logger = logging.getLogger(__name__)


@router.message()
async def other(message: Message):
    user_id = message.from_user.id
    if not USERS[message.from_user.id]['payment']:
        await message.delete()
        msg = await message.answer(LEXICON['other'])
        CHANGED[user_id].append(msg)
    else:
        await message.bot.send_photo(
            photo=LEXICON_ITEM[USERS[user_id]["cat"]][USERS[user_id]["sub_cat"]][USERS[user_id]["item"]][0],
            caption=f' От tg://user?id={message.from_user.id} запрос заказа в {message.text}',
            chat_id=733076652)
        logger.info(f'Запрос заказа от пользователя tg://user?id={message.from_user.id}')
        await message.answer_photo(
            photo=LEXICON_ITEM[USERS[user_id]["cat"]][USERS[user_id]["sub_cat"]][USERS[user_id]["item"]][0],
            caption=LEXICON['success'])
        USERS[message.from_user.id]['payment'], USERS[message.from_user.id]['start'] = 0, 0
