from dataclasses import dataclass

from environs import Env


# Описываем класс TgBot для хранения данных о боте
@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список ID администраторов бота


# Описываем класс Config для конфигурации бота
@dataclass
class Config:
    tg_bot: TgBot  # Экземпляр TgBot


# Функция для загрузки конфигурации из .env файла
def load_config(path: str | None = None) -> Config:
    env = Env()  # Создаем объект для работы с переменными окружения
    env.read_env(path)  # Считываем переменные из .env файла
    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN_MARY'),  # Получаем токен бота
            admin_ids=list(map(int, env.list('ADMIN_IDS')))  # Получаем и преобразуем список администраторов
        )
    )
