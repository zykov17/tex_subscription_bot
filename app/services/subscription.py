from aiogram import Bot
from aiogram.types import ChatMember
from aiogram.exceptions import TelegramAPIError
import logging

from config import config

logger = logging.getLogger(__name__)

async def check_subscription(bot: Bot, user_id: int) -> bool:
    """
    Проверяет, подписан ли пользователь на указанный канал
    
    Args:
        bot: Экземпляр бота
        user_id: ID пользователя для проверки
    
    Returns:
        bool: True если подписан, False если нет или произошла ошибка
    """
    try:
        # Получаем информацию о статусе пользователя в канале
        member = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=user_id)
        
        # Проверяем, что статус пользователя является одним из "активных"
        # 'member', 'administrator', 'creator' - пользователь подписан
        # 'left', 'kicked', 'restricted' - пользователь не подписан или забанен
        return member.status in ['member', 'administrator', 'creator']
    
    except TelegramAPIError as e:
        logger.error(f"Ошибка Telegram API при проверке подписки: {e}")
        # В случае ошибки API считаем, что пользователь не подписан
        return False
    
    except Exception as e:
        logger.error(f"Неожиданная ошибка при проверке подписки: {e}")
        return False