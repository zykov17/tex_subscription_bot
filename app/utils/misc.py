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
            created_at = user.created_at
            if created_at:
                # Преобразуем в строку
                if hasattr(created_at, 'strftime'):
                    created_at_str = created_at.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    created_at_str = str(created_at)
            else:
                created_at_str = 'N/A'
            
            writer.writerow([
                user.user_id,
                user.username or 'N/A',
                user.first_name or 'N/A',
                user.gift_code or 'N/A',
                created_at_str
            ])
        
        # Перемещаем указатель в начало
        output.seek(0)
        return output
    
    except Exception as e:
        logger.error(f"Ошибка при генерации CSV: {e}")
        # Возвращаем пустой StringIO в случае ошибки
        empty_output = io.StringIO()
        writer = csv.writer(empty_output)
        writer.writerow(['Error', 'Failed to generate CSV data'])
        empty_output.seek(0)
        return empty_output