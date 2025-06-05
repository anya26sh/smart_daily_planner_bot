from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from keyboards.inline import main_menu, tasks_keyboard, back_button
from services.database import db
from utils.formatters import format_tasks_list
from states.user_states import TaskStates
from filters.task_filter import TaskCallbackFilter
from utils.logger import logger

router = Router()

@router.callback_query(F.data == "add_task")
async def add_task_start(callback: CallbackQuery, state: FSMContext):
    """начало добавления задачи"""
    await callback.message.edit_text(
        "📝 Введите текст новой задачи:",
        reply_markup=back_button()
    )
    await state.set_state(TaskStates.waiting_task)
    await callback.answer()

@router.message(TaskStates.waiting_task)
async def add_task_finish(message: Message, state: FSMContext):
    """завершение добавления задачи"""
    task_text = message.text.strip()
    
    if len(task_text) > 200:
        await message.answer("❌ Задача слишком длинная! Максимум 200 символов.")
        return
    
    success = await db.add_task(message.from_user.id, task_text)
    
    if success:
        await message.answer(
            f"✅ Задача добавлена: _{task_text}_",
            reply_markup=main_menu()
        )
    else:
        await message.answer("❌ Ошибка при добавлении задачи")
    
    await state.clear()

@router.callback_query(F.data == "show_tasks")
async def show_tasks(callback: CallbackQuery):
    """показ списка задач"""
    tasks = await db.get_tasks(callback.from_user.id)
    text = format_tasks_list(tasks)
    
    if tasks:
        keyboard = tasks_keyboard(tasks)
    else:
        keyboard = back_button()
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(TaskCallbackFilter("complete_"))
async def complete_task(callback: CallbackQuery):
    """завершение задачи"""
    task_id = int(callback.data.split("_")[1])
    success = await db.complete_task(callback.from_user.id, task_id)
    
    if success:
        await callback.answer("✅ Задача выполнена!", show_alert=True)
        # обновляем список задач
        tasks = await db.get_tasks(callback.from_user.id)
        text = format_tasks_list(tasks)
        
        if tasks:
            keyboard = tasks_keyboard(tasks)
        else:
            keyboard = back_button()
        
        await callback.message.edit_text(text, reply_markup=keyboard)
    else:
        await callback.answer("❌ Ошибка при выполнении задачи")