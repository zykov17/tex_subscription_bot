from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
import logging
import aiofiles
import os

from app.models.user import User
from config import config

logger = logging.getLogger(__name__)

async def has_received_gift(session: AsyncSession, user_id: int) -> bool:
    """
    Проверяет, получал ли пользователь подарок ранее
    
    Args:
        session: Асинхронная сессия БД
        user_id: ID пользователя для проверки
    
    Returns:
        bool: True если пользователь уже получал подарок
    """
    try:
        result = await session.execute(
            select(User).where(User.user_id == user_id)
        )
        user = result.scalar_one_or_none()
        return user is not None
    
    except SQLAlchemyError as e:
        logger.error(f"Ошибка базы данных при проверке подарка: {e}")
        # В случае ошибки БД считаем, что пользователь уже получал подарок
        # чтобы предотвратить множественную выдачу
        return True

async def save_gift_recipient(session: AsyncSession, user_id: int, username: str, first_name: str) -> User:
    """
    Сохраняет информацию о пользователе, получившем подарок
    
    Args:
        session: Асинхронная сессия БД
        user_id: ID пользователя
        username: Username пользователя
        first_name: Имя пользователя
    
    Returns:
        User: Созданный объект пользователя
    """
    try:
        # Генерируем уникальный промокод
        gift_code = f"GIFT{user_id:08d}"
        
        # Создаем нового пользователя
        new_user = User(
            user_id=user_id,
            username=username,
            first_name=first_name,
            gift_code=gift_code
        )
        
        # Добавляем в сессию и сохраняем
        session.add(new_user)
        await session.commit()
        
        logger.info(f"Пользователь {user_id} сохранен в базе данных")
        return new_user
    
    except SQLAlchemyError as e:
        await session.rollback()
        logger.error(f"Ошибка при сохранении пользователя в БД: {e}")
        raise

async def get_gift_content() -> tuple:
    """
    Получает контент подарка в зависимости от конфигурации
    
    Returns:
        tuple: (тип_контента, содержимое)
        Типы: 'text' или 'document'
    """
    if config.GIFT_FILE_PATH and os.path.exists(config.GIFT_FILE_PATH):
        # Если указан путь к файлу и файл существует - отправляем файл
        return 'document', config.GIFT_FILE_PATH
    else:
        # Иначе отправляем текстовый промокод
        return 'text', config.GIFT_TEXT

async def get_all_recipients(session: AsyncSession) -> list:
    """
    Получает список всех пользователей, получивших подарок
    
    Args:
        session: Асинхронная сессия БД
    
    Returns:
        list: Список объектов User
    """
    try:
        result = await session.execute(select(User).order_by(User.created_at.desc()))
        users = result.scalars().all()
        return users
    
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении списка пользователей: {e}")
        return []