from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import back_button
from services.database import db
from utils.formatters import format_stats
from services.api_client import api_client

router = Router()

@router.callback_query(F.data == "show_stats")
async def show_user_stats(callback: CallbackQuery):
    """показ статистики пользователя"""
    stats = await db.get_stats(callback.from_user.id)
    text = format_stats(stats)
    
    await callback.message.edit_text(text, reply_markup=back_button())
    await callback.answer()

@router.callback_query(F.data == "quote")
async def show_quote(callback: CallbackQuery):
    """показ цитаты"""
    quote = await api_client.get_quote()
    
    if quote:
        text = f"💭 **Цитата дня:**\n\n_{quote}_"
    else:
        text = "❌ Не удалось получить цитату"
    
    await callback.message.edit_text(text, reply_markup=back_button())
    await callback.answer()