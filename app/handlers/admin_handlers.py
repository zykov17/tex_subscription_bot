from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError
import logging
from datetime import datetime

from config import config
from app.keyboards.inline_kb import create_admin_keyboard
from app.services.gift_service import get_all_recipients
from app.utils.misc import generate_csv_data
from app.models.database import db

logger = logging.getLogger(__name__)

# Создаем роутер для административных handlers
admin_router = Router()


# Фильтр для проверки прав администратора
def is_admin(user_id: int) -> bool:
    """Проверяет, является ли пользователь администратором"""
    return config.ADMIN_ID and user_id == config.ADMIN_ID


@admin_router.message(Command("admin"))
async def cmd_admin(message: Message):
    """
    Обработчик команды /admin
    """
    if not is_admin(message.from_user.id):
        await message.answer("⛔ У вас нет прав доступа к админ-панели.")
        return
    
    await message.answer(
        "👨‍💻 Панель администратора\n\n"
        "Выберите действие:",
        reply_markup=create_admin_keyboard()
    )


@admin_router.callback_query(F.data == "admin_stats")
async def admin_stats_callback(callback: CallbackQuery):
    """
    Показывает статистику выданных подарков
    """
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет прав доступа")
        return
    
    try:
        session = await db.get_session()
        try:
            users = await get_all_recipients(session)

            await callback.message.edit_text(
                f"📊 Статистика подарков:\n\n"
                f"• Всего выдано: {len(users)} подарков\n"
                f"• Последняя выдача: {users[0].created_at.strftime('%Y-%m-%d %H:%M') if users else 'N/A'}\n\n"
                "Для экспорта данных нажмите кнопку ниже:",
                reply_markup=create_admin_keyboard()
            )
        finally:
            await session.close()

        await callback.answer()
    
    except Exception as e:
        logger.error(f"Ошибка при получении статистики: {e}")
        await callback.answer("⚠️ Ошибка при получении статистики")


@admin_router.callback_query(F.data == "admin_export")
async def admin_export_callback(callback: CallbackQuery):
    """
    Экспортирует данные о пользователях в CSV файл
    """
    if not is_admin(callback.from_user.id):
        await callback.answer("⛔ Нет прав доступа")
        return
    
    try:
        session = await db.get_session()
        try:
            users = await get_all_recipients(session)

            if not users:
                await callback.message.answer("📭 Нет данных для экспорта.")
                await callback.answer()
                return

            # Генерируем CSV данные
            csv_string_io = generate_csv_data(users)
            csv_content = csv_string_io.getvalue()

            # Создаем BufferedInputFile из содержимого CSV
            csv_file = BufferedInputFile(
                file=csv_content.encode("utf-8"),
                filename=f"gift_recipients_{len(users)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            )

            # Отправляем файл
            await callback.message.answer_document(
                document=csv_file,
                caption=f"📁 Экспорт данных\nВыдано подарков: {len(users)}"
            )
        finally:
            await session.close()

        await callback.answer("✅ Данные экспортированы")
    
    except Exception as e:
        logger.error(f"Ошибка при экспорте данных: {e}")
        await callback.answer("⚠️ Ошибка при экспорте данных")
