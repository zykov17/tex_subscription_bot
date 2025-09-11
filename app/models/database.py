from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import asyncio

from config import config
from .user import Base

class Database:
    """Класс для работы с базой данных"""
    
    def __init__(self):
        self.engine = None
        self.async_session = None
    
    async def init(self):
        """Инициализация подключения к базе данных"""
        try:
            # Создаем асинхронный движок для работы с БД
            self.engine = create_async_engine(
                config.DATABASE_URL,
                echo=False,  # Включаем для отладки SQL запросов
                future=True
            )
            
            # Создаем фабрику сессий
            self.async_session = sessionmaker(
                self.engine, class_=AsyncSession, expire_on_commit=False
            )
            
            # Создаем таблицы в базе данных
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            
            print("База данных успешно инициализирована")
            
        except Exception as e:
            print(f"Ошибка при инициализации базы данных: {e}")
            raise
    
    async def get_session(self) -> AsyncSession:
        """Получение асинхронной сессии для работы с БД"""
        if not self.async_session:
            await self.init()
        
        async with self.async_session() as session:
            try:
                yield session
            finally:
                await session.close()
    
    async def close(self):
        """Закрытие соединения с базой данных"""
        if self.engine:
            await self.engine.dispose()
            print("Соединение с базой данных закрыто")

# Глобальный экземпляр базы данных
db = Database()