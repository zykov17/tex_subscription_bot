from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError
import logging

from config import config
from app.keyboards.inline_kb import create_subscription_keyboard, create_contacts_keyboard
from app.services.subscription import check_subscription
from app.services.gift_service import has_received_gift, save_gift_recipient, get_gift_content
from app.models.database import db

logger = logging.getLogger(__name__)

# Создаем роутер для пользовательских handlers
user_router = Router()


@user_router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    try:
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name

        logger.info(f"Пользователь {user_id} запустил бота")

        # Получаем сессию БД
        session = await db.get_session()
        try:
            # Проверяем, получал ли пользователь подарок ранее
            if await has_received_gift(session, user_id):
                await message.answer(
                    "🎁 Вы уже получали подарок ранее! Спасибо за участие!",
                    reply_markup=create_contacts_keyboard()
                )
                return

            # Проверяем подписку на канал
            is_subscribed = await check_subscription(message.bot, user_id)

            if is_subscribed:
                # Если подписан - выдаем подарок
                await handle_gift_delivery(message, session, user_id, username, first_name)
            else:
                # Если не подписан - просим подписаться
                await message.answer(
                    f"👋 Привет, {first_name}!\n\n"
                    f"Чтобы получить подарок, подпишитесь на наш канал: <a href='https://t.me/{config.CHANNEL_USERNAME}'>Текстилия</a>\n\n"
                    "После подписки нажмите кнопку ниже для проверки:",
                    reply_markup=create_subscription_keyboard(),
                    parse_mode="HTML"
                )
        finally:
            await session.close()

    except Exception as e:
        logger.error(f"Ошибка в обработчике /start: {e}")
        await message.answer("⚠️ Произошла ошибка. Пожалуйста, попробуйте позже.")


@user_router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery):
    """Обработчик callback для проверки подписки"""
    try:
        user_id = callback.from_user.id
        username = callback.from_user.username
        first_name = callback.from_user.first_name

        # Отвечаем на callback, чтобы убрать "часики" у кнопки
        await callback.answer()

        # Получаем сессию
        session = await db.get_session()
        try:
            # Проверяем подписку
            is_subscribed = await check_subscription(callback.bot, user_id)

            if is_subscribed:
                # Если подписан - выдаем подарок
                await handle_gift_delivery(callback.message, session, user_id, username, first_name)
            else:
                # Если все еще не подписан - просим подписаться снова
                await callback.message.answer(
                    "❌ Вы еще не подписались на канал.\n\n"
                    f"Пожалуйста, подпишитесь на канал <a href='https://t.me/{config.CHANNEL_USERNAME}'>Текстилия</a> и нажмите проверку снова:",
                    reply_markup=create_subscription_keyboard(),
                    parse_mode="HTML"
                )
        finally:
            await session.close()

    except TelegramAPIError as e:
        logger.error(f"Ошибка Telegram API при проверке подписки: {e}")
        await callback.message.answer("⚠️ Ошибка проверки подписки. Попробуйте позже.")
    except Exception as e:
        logger.error(f"Ошибка в обработчике проверки подписки: {e}")
        await callback.message.answer("⚠️ Произошла ошибка. Пожалуйста, попробуйте позже.")


async def handle_gift_delivery(message: Message, session, user_id: int, username: str, first_name: str):
    """Обрабатывает выдачу подарка пользователю"""
    try:
        # Сохраняем информацию о пользователе
        user = await save_gift_recipient(session, user_id, username, first_name)

        # Получаем контент подарка
        gift_type, gift_content = await get_gift_content()

        # Отправляем подарок пользователю
        if gift_type == 'document':
            with open(gift_content, 'rb') as file:
                await message.answer_document(
                    document=file,
                    caption=f"🎉 Поздравляем, {first_name}!\n\n"
                            "Ваш подарок готов! Спасибо за подписку!\n\n"
                            f"Ваш промокод: {user.gift_code}"
                )
        else:
            await message.answer(
                f"🎉 Поздравляем, {first_name}!\n\n"
                f"Ваш подарок: {gift_content}\n\n"
                "Спасибо за подписку!",
                reply_markup=None
            )

        logger.info(f"Пользователь {user_id} успешно получил подарок")
    except Exception as e:
        logger.error(f"Ошибка при выдаче подарка: {e}")
        await message.answer("⚠️ Произошла ошибка при выдаче подарка. Пожалуйста, попробуйте позже.")
