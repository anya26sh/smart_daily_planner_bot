from aiogram.filters.callback_data import CallbackData
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

class TaskCallbackFilter(BaseFilter):
    def __init__(self, prefix: str):
        self.prefix = prefix
    
    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data and callback.data.startswith(self.prefix)