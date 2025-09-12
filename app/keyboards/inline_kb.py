from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import config

def create_subscription_keyboard() -> InlineKeyboardMarkup:
    """
    Создает инлайн-клавиатуру для подписки на канал и проверки
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📢 Подписаться на канал",
                url=f"https://t.me/{config.CHANNEL_USERNAME.lstrip('@')}"
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Я подписался! Проверить",
                callback_data="check_subscription"
            )
        ]
    ])
    return keyboard

def create_admin_keyboard() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для администратора
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats"),
            InlineKeyboardButton(text="📁 Экспорт данных", callback_data="admin_export")
        ]
    ])
    return keyboard

def create_contacts_keyboard() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру контактов
    """
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="📢 Перейти в канал",
                url=f"https://t.me/{config.CHANNEL_USERNAME.lstrip('@')}"
            ),
            InlineKeyboardButton(
                text = "📢 Перейти на сайт",
                url = config.SITE_URL
            ),
        ]
    ])
    return keyboard