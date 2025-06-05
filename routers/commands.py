from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from keyboards.inline import main_menu, back_button
from services.database import db
from services.api_client import api_client
from utils.logger import logger

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """команда /start"""
    await db.add_task(message.from_user.id, "Изучить возможности бота")
    text = f"""👋 Привет, {message.from_user.first_name}!

🤖 Я умный ежедневник, который поможет вам:
- Управлять задачами
- Отслеживать прогресс  
- Получать мотивацию

📝 Я уже добавил вам первую задачу для знакомства с ботом!"""
    
    await message.answer(text, reply_markup=main_menu())
    logger.info(f"новый пользователь: {message.from_user.id}")

@router.message(Command("help"))
async def cmd_help(message: Message):
    """команда /help"""
    text = """❓ **Справка по командам:**

/start - запуск бота
/help - эта справка
/menu - главное меню
/quote - получить цитату дня

🔥 **Основные возможности:**
- Добавление и управление задачами
- Статистика выполнения
- Мотивационные цитаты"""
    
    await message.answer(text, reply_markup=back_button())

@router.message(Command("menu"))
async def cmd_menu(message: Message):
    """команда /menu"""
    await message.answer("🏠 Главное меню:", reply_markup=main_menu())

@router.message(Command("quote"))
async def cmd_quote(message: Message):
    """команда /quote"""
    quote = await api_client.get_quote()
    if quote:
        await message.answer(f"💭 **Цитата дня:**\n\n_{quote}_")
    else:
        await message.answer("❌ Не удалось получить цитату. Попробуйте позже.")

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    """возврат в главное меню"""
    await callback.message.edit_text("🏠 Главное меню:", reply_markup=main_menu())
    await callback.answer()