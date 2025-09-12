import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Config:
    """Класс для хранения конфигурационных параметров"""

    # Токен бота, полученный от @BotFather
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден в переменных окружения")

    # ID канала для проверки подписки
    CHANNEL_ID = os.getenv("CHANNEL_ID")
    if not CHANNEL_ID:
        raise ValueError("CHANNEL_ID не найден в переменных окружения")

    # username канала для генерации ссылки
    CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")
    if not CHANNEL_USERNAME:
        raise ValueError("CHANNEL_USERNAME не найден в переменных окружения")

    # username бота для ссылки на менеджеров
    MANAGER_BOT_USERNAME = os.getenv("MANAGER_BOT_USERNAME")
    if not MANAGER_BOT_USERNAME:
        raise ValueError("MANAGER_BOT_USERNAME не найден в переменных окружения")

    # ID администратора для доступа к админ-панели
    ADMIN_ID = os.getenv('ADMIN_ID')
    if ADMIN_ID:
        ADMIN_ID = int(ADMIN_ID)

    # URL сайта
    SITE_URL = os.getenv('SITE_URL')

    # URL для подключения к базе данных
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite+aiosqlite://data/database.db')

    # Путь к файлу подарка (если используется)
    GIFT_FILE_PATH = os.getenv('GIFT_FILE_PATH')

    # Текст подарка (если используется текстовый промокод)
    GIFT_TEXT = os.getenv('GIFT_TEXT', 'Ваш промокод: THANKYOU2024')

    # Создаем директорию для данных, если она не существует
    if not os.path.exists('data'):
        os.makedirs('data')

# Создаем экземпляр конфигурации
config = Config()