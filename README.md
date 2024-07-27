# Шаблон Telegram бота для оформления заказов на примере заказа картин 🎨

Этот Telegram бот позволяет пользователям заказывать авторские картины, взаимодействуя с ботом. Он проводит пользователей через серию шагов для выбора категорий, подкатегорий и конкретных товаров, а затем оформления заказа. Бот также поддерживает функции администрирования для управления товарами.

## 🌟 Функциональные возможности

- **Взаимодействие с пользователем**: Пользователи могут запускать бота, выбирать категории, подкатегории и товары, а затем оформлять заказы. 🛒
- **Взаимодействие с администратором**: Администраторы могут добавлять новые товары в бот. 🛠️
- **Логирование**: Бот ведет журнал всех действий для мониторинга и отладки. 📋
- **Обработка ошибок**: Базовая обработка ошибок для управления взаимодействием пользователей и администраторов с ботом. 🚨

## 🛠️ Установка и настройка

1. Клонируйте репозиторий:
    ```sh
    git clone https://github.com/yourusername/yourbotrepo.git
    cd yourbotrepo
    ```
2. Установите необходимые пакеты:
    ```sh
    pip install -r requirements.txt
    ```
3. Настройте конфигурацию:
    - Создайте файл `.env` в корневом каталоге и добавьте ваш токен бота и другие настройки.
    - Пример:
      ```env
      TG_BOT_TOKEN=your-telegram-bot-token
      ```
4. Запустите бота:
    ```sh
    python main.py
    ```

## Конфигурация

Бот использует файл конфигурации для управления настройками, такими как токен бота и ID администраторов. Конфигурация загружается из файла `.env`.

## Обзор кода

### `main.py`

Основной скрипт для настройки и запуска бота:
- Инициализирует логирование 📋
- Загружает конфигурацию ⚙️
- Настраивает бота и диспетчер 🤖
- Регистрирует обработчики для пользователей и администраторов 👥
- Начинает опрос сообщений 📨

### Обработчики

- **`user_handlers.py`**: Управляет командами и взаимодействием с пользователями. 👤
- **`admin_handlers.py`**: Управляет командами администраторов для добавления новых товаров. 🛠️
- **`other_handlers.py`**: Обрабатывает другие типы сообщений и взаимодействий. 💬

### Клавиатуры

- **`main_menu.py`**: Определяет структуру главного меню бота. 📜

### Лексикон

- **`lexicon.py`**: Содержит текстовые ответы и сообщения, используемые ботом. 🗣️

### Сервисы

- **`file_handling.py`**: Обрабатывает файловые операции и пользовательские фильтры для проверки администратора. 📂

### База данных

- **`database.py`**: Управляет хранилищем в памяти для пользовательских сессий и данных о товарах. 🗃️

## 📚 Использование

### Команды для пользователей

- `/start`: Начать взаимодействие с ботом. 🚀
- `/help`: Получить помощь и список команд. ❓
- `/contacts`: Получить контактную информацию. 📞
- `/reset`: Сбросить текущую сессию и начать заново. 🔄

### Команды для администраторов

- **Добавление новых товаров путем отправки фотографий с подписями, содержащими информацию о категории и подкатегории.** 🖼️

### Пример взаимодействия

1. Пользователь запускает бота командой `/start`. 🚀
2. Бот предлагает выбрать категорию. 📋
3. Пользователь выбирает категорию, затем подкатегорию и, наконец, товар. 🎨
4. Пользователь предоставляет необходимые данные и оформляет заказ. 📝
5. Бот подтверждает заказ и предоставляет контактную информацию для дальнейшего общения. 📞

## Вклад в проект

Если вы хотите внести свой вклад в проект, пожалуйста, форкните репозиторий и отправьте pull request. Все вклады приветствуются! 🤝

## 📧 Контакты
Для вопросов или предложений, свяжитесь с нами по адресу Andreireut0@gmail.com или по телеграмму: https://t.me/and_reut.
