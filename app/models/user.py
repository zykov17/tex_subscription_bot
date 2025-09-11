from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()

class User(Base):
    """Модель пользователя для хранения информации о выданных подарках"""
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False, unique=True)  # Telegram user ID
    username = Column(String(100))  # Telegram username (может быть None)
    first_name = Column(String(100))  # Имя пользователя
    created_at = Column(DateTime, default=lambda: datetime.now(pytz.UTC))  # Время получения подарка
    gift_code = Column(String(50))  # Выданный промокод (опционально)
    
    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}')>"
    
    def to_dict(self):
        """Преобразование объекта в словарь для экспорта"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'gift_code': self.gift_code
        }