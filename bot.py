import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import config
from app.models.database import db
from app.handlers.user_handlers import user_router
from app.handlers.admin_handlers import admin_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def main():
    """Основная функция запуска бота"""
    
    # Инициализация базы данных
    try:
        await db.init()
        logger.info("База данных инициализирована")
    except Exception as e:
        logger.error(f"Ошибка инициализации БД: {e}")
        return
    
    # Создаем экземпляр бота с настройками по умолчанию
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Создаем диспетчер
    dp = Dispatcher()
    
    # Включаем роутеры
    dp.include_router(user_router)
    dp.include_router(admin_router)
    
    # Запускаем опрос обновлений
    try:
        logger.info("Бот запущен")
        await dp.start_polling(bot)
    
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {e}")
    
    finally:
        # Закрываем соединение с БД при завершении
        await db.close()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    # Запускаем асинхронную функцию main
    asyncio.run(main())