from typing import Dict, List

def format_tasks_list(tasks: List[Dict]) -> str:
    """форматирование списка задач"""
    if not tasks:
        return "📝 У вас пока нет активных задач"
    
    text = "📋 **Ваши активные задачи:**\n\n"
    for i, task in enumerate(tasks, 1):
        text += f"{i}. {task['text']}\n"
    
    text += "\n💡 Нажмите на задачу, чтобы отметить её выполненной"
    return text

def format_stats(stats: Dict[str, int]) -> str:
    """форматирование статистики"""
    return f"""📊 **Ваша статистика:**

📝 Активных задач: {stats['active']}
✅ Выполнено задач: {stats['completed']}
📈 Всего создано: {stats['total']}"""