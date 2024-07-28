import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from config_data.config import load_config
from handlers import user_handlers, other_handlers, admin_handlers
from keyboards.main_menu import set_main_menu

# Инициализация логгера
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурирование логирования
    logging.basicConfig(level=logging.INFO)  # Установка уровня логирования
    formatter = logging.Formatter('%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s')
    file_handler = logging.FileHandler('bot_logs.log', mode='w', encoding='utf-8')  # Создание обработчика логов
    file_handler.setFormatter(formatter)  # Установка формата логов
    logger.addHandler(file_handler)  # Добавление обработчика к логгеру

    # Вывод информации о начале запуска бота
    logger.info('Starting bot')

    # Загрузка конфигурации из файла .env
    config = load_config('.env')

    # Инициализация объекта хранилища (при необходимости)
    # storage = ...

    # Инициализация бота и диспетчера
    default = DefaultBotProperties(parse_mode='HTML')  # Установка свойств по умолчанию для бота
    bot = Bot(token=config.tg_bot.token, default=default)  # Создание объекта бота
    dp = Dispatcher()  # Создание объекта диспетчера

    # Инициализация других объектов (пул соединений с БД, кеш и т.п.)
    # ...

    # Помещение нужных объектов в workflow_data диспетчера
    dp.workflow_data.update({'token': config.tg_bot.token, 'admin_ids': config.tg_bot.admin_ids})

    # Настройка главного меню бота
    await set_main_menu(bot)

    # Регистрация роутеров
    logger.info('Подключаем роутеры')
    dp.include_router(admin_handlers.router)  # Подключение роутера для администраторов
    dp.include_router(user_handlers.router)  # Подключение роутера для пользователей
    dp.include_router(other_handlers.router)  # Подключение других роутеров

    # Удаление вебхука и запуск polling
    await bot.delete_webhook(drop_pending_updates=True)  # Удаление вебхука и удаление ожидающих обновлений
    await dp.start_polling(bot)  # Запуск поллинга


# Запуск main при запуске скрипта
if __name__ == '__main__':
    asyncio.run(main())
