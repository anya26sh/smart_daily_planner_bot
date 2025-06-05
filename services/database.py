import json
import aiofiles
import os
from typing import List, Dict, Optional
from config.settings import config
from utils.logger import logger

class Database:
    def __init__(self):
        self.tasks_file = config.tasks_file
        self._ensure_storage_dir()
    
    def _ensure_storage_dir(self):
        """создание директории storage если её нет"""
        os.makedirs(os.path.dirname(self.tasks_file), exist_ok=True)
    
    async def _load_data(self) -> Dict:
        """загрузка данных из файла"""
        try:
            if os.path.exists(self.tasks_file):
                async with aiofiles.open(self.tasks_file, 'r', encoding='utf-8') as f:
                    content = await f.read()
                    return json.loads(content) if content.strip() else {}
            return {}
        except Exception as e:
            logger.error(f"ошибка загрузки данных: {e}")
            return {}
    
    async def _save_data(self, data: Dict):
        """сохранение данных в файл"""
        try:
            async with aiofiles.open(self.tasks_file, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(data, ensure_ascii=False, indent=2))
        except Exception as e:
            logger.error(f"ошибка сохранения данных: {e}")
    
    async def add_task(self, user_id: int, task_text: str) -> bool:
        """добавление новой задачи"""
        try:
            data = await self._load_data()
            
            if str(user_id) not in data:
                data[str(user_id)] = {
                    "tasks": [],
                    "completed": 0,
                    "next_id": 1
                }
            
            user_data = data[str(user_id)]
            task = {
                "id": user_data["next_id"],
                "text": task_text,
                "created_at": str(datetime.now())
            }
            
            user_data["tasks"].append(task)
            user_data["next_id"] += 1
            
            await self._save_data(data)
            logger.info(f"пользователь {user_id} добавил задачу: {task_text}")
            return True
        except Exception as e:
            logger.error(f"ошибка добавления задачи: {e}")
            return False
    
    async def get_tasks(self, user_id: int) -> List[Dict]:
        """получение активных задач пользователя"""
        try:
            data = await self._load_data()
            user_data = data.get(str(user_id), {})
            return user_data.get("tasks", [])
        except Exception as e:
            logger.error(f"ошибка получения задач: {e}")
            return []
    
    async def complete_task(self, user_id: int, task_id: int) -> bool:
        """завершение задачи"""
        try:
            data = await self._load_data()
            
            if str(user_id) not in data:
                return False
            
            user_data = data[str(user_id)]
            tasks = user_data.get("tasks", [])
            
            # поиск и удаление задачи
            for i, task in enumerate(tasks):
                if task["id"] == task_id:
                    tasks.pop(i)
                    user_data["completed"] += 1
                    await self._save_data(data)
                    logger.info(f"пользователь {user_id} завершил задачу {task_id}")
                    return True
            
            return False
        except Exception as e:
            logger.error(f"ошибка завершения задачи: {e}")
            return False
    
    async def get_stats(self, user_id: int) -> Dict[str, int]:
        """получение статистики пользователя"""
        try:
            data = await self._load_data()
            user_data = data.get(str(user_id), {})
            
            active_tasks = len(user_data.get("tasks", []))
            completed_tasks = user_data.get("completed", 0)
            
            return {
                "active": active_tasks,
                "completed": completed_tasks,
                "total": active_tasks + completed_tasks
            }
        except Exception as e:
            logger.error(f"ошибка получения статистики: {e}")
            return {"active": 0, "completed": 0, "total": 0}

# импорт datetime
from datetime import datetime

db = Database()