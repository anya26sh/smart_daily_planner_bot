from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import List, Dict

def main_menu() -> InlineKeyboardMarkup:
    """главное меню"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📝 Добавить задачу", callback_data="add_task"))
    builder.add(InlineKeyboardButton(text="📋 Мои задачи", callback_data="show_tasks"))
    builder.add(InlineKeyboardButton(text="📊 Статистика", callback_data="show_stats"))
    builder.add(InlineKeyboardButton(text="💭 Цитата дня", callback_data="quote"))
    builder.adjust(2, 2)
    return builder.as_markup()

def tasks_keyboard(tasks: List[Dict]) -> InlineKeyboardMarkup:
    """клавиатура со списком задач"""
    builder = InlineKeyboardBuilder()
    
    for task in tasks:
        text = f"✅ {task['text'][:30]}..." if len(task['text']) > 30 else f"✅ {task['text']}"
        builder.add(InlineKeyboardButton(
            text=text, 
            callback_data=f"complete_{task['id']}"
        ))
    
    builder.add(InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu"))
    builder.adjust(1)
    return builder.as_markup()

def back_button() -> InlineKeyboardMarkup:
    """кнопка назад"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🔙 Главное меню", callback_data="back_to_menu"))
    return builder.as_markup()