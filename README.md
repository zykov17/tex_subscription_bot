Tex Subscription Bot

Телеграм-бот для выдачи подарков пользователям после проверки подписки на Telegram-канал.

Цель проекта: автоматизировать процесс выдачи промокодов или файлов подарков новым подписчикам канала.

📌 Основной функционал

Проверяет, подписан ли пользователь на указанный Telegram-канал.

Если пользователь не подписан — предлагает подписаться и выводит кнопку с ссылкой на канал.

После подписки пользователь проходит повторную проверку.

Если подписка подтверждена — бот выдает подарок:

промокод (текст)

PDF-файл или другой документ

Один пользователь не может получить подарок повторно.

Администратор может просматривать список пользователей, получивших подарок.

Любые непредусмотренные сообщения или действия пользователя вызывают уведомление, что бот ограничен и следует использовать кнопки и команды.

⚙️ Структура проекта
tex_subscription_bot/
│
├── bot.py                 # Точка входа, запуск бота
├── config.py              # Конфигурация проекта
├── requirements.txt       # Зависимости Python
└── app/
    ├── __init__.py
    ├── handlers/
    │   ├── __init__.py
    │   └── user_handlers.py      # Основные обработчики команд и callback
    ├── keyboards/
    │   ├── __init__.py
    │   ├── inline_kb.py          # Inline-клавиатуры (подписка, проверка)
    │   └── reply_kb.py           # Reply-клавиатуры (контакты)
    ├── models/
    │   ├── __init__.py
    │   ├── database.py           # Подключение к БД, создание сессий
    │   └── user.py               # Модель User для хранения подарков
    └── services/
        ├── __init__.py
        ├── gift_service.py       # Работа с подарками
        └── subscription.py       # Проверка подписки на канал

📝 Установка и запуск
1. Клонирование репозитория
git clone https://github.com/zykov17/tex_subscription_bot.git
cd tex_subscription_bot

2. Создание виртуального окружения
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
.venv\Scripts\activate         # Windows

3. Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

4. Настройка конфигурации

Создайте .env файл или редактируйте config.py:
BOT_TOKEN = "ВАШ_ТОКЕН_БОТА"
CHANNEL_USERNAME = "tkani_textiliya"
DATABASE_URL = "sqlite+aiosqlite:///db.sqlite3"  # или PostgreSQL
GIFT_TEXT = "PROMO1234"
GIFT_FILE_PATH = "path/to/gift.pdf"
ADMIN_IDS = [123456789]

5. Инициализация базы данных

База данных создается автоматически при первом запуске бота.

6. Запуск бота
python bot.py

🟢 Использование

/start — приветствие и запуск проверки подписки.

Кнопка "📢 Подписаться на канал" — открывает канал.

Кнопка "Проверить подписку" — проверяет подписку и выдает подарок.

Непредусмотренные сообщения вызывают уведомление:
🤖 Это ограниченный бот. Пожалуйста, используйте доступные кнопки и команды.

Для администраторов:

Список пользователей, получивших подарок, доступен через get_all_recipients() в gift_service.py.

🗄️ База данных

Таблица users хранит информацию о получателях подарков:

Поле	Тип	Описание
id	INTEGER PK	Уникальный идентификатор записи
user_id	BIGINT	Telegram ID пользователя
username	STRING	Username пользователя
first_name	STRING	Имя пользователя
created_at	DATETIME	Дата выдачи подарка
gift_code	STRING	Промокод или ссылка на подарок

📦 Модули
gift_service.py

has_received_gift(session, user_id) — проверка, получал ли пользователь подарок.

save_gift_recipient(session, user_id, username, first_name) — сохраняет пользователя.

get_gift_content() — возвращает текст или файл подарка.

get_all_recipients(session) — список всех пользователей.

subscription.py

Проверка подписки через Telegram API: is_member = bot.get_chat_member(channel_id, user_id).

user_handlers.py

Обработчики /start и check_subscription.

Фолбэк на непредусмотренные сообщения и callback.