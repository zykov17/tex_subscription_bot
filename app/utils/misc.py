import csv
import io
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def generate_csv_data(users: list) -> io.StringIO:
    """
    Генерирует CSV файл с данными пользователей
    
    Args:
        users: Список объектов User
    
    Returns:
        io.StringIO: Поток с CSV данными
    """
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Записываем заголовки
        writer.writerow(['User ID', 'Username', 'First Name', 'Gift Code', 'Created At'])
        
        # Записываем данные пользователей
        for user in users:
            writer.writerow([
                user.user_id,
                user.username or 'N/A',
                user.first_name or 'N/A',
                user.gift_code or 'N/A',
                user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else 'N/A'
            ])
        
        # Перемещаем указатель в начало
        output.seek(0)
        return output
    
    except Exception as e:
        logger.error(f"Ошибка при генерации CSV: {e}")
        raise