import asyncio
from typing import Dict, Any
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.last_action: Dict[int, float] = {}
    
    async def __call__(
        self,
        handler,
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        current_time = asyncio.get_event_loop().time()
        
        if user_id in self.last_action:
            time_passed = current_time - self.last_action[user_id]
            if time_passed < self.rate_limit:
                if isinstance(event, CallbackQuery):
                    await event.answer("Не так быстро! Подождите немного.", show_alert=True)
                return
        
        self.last_action[user_id] = current_time
        return await handler(event, data)