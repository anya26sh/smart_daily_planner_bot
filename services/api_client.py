import aiohttp
import asyncio
import random
from typing import Optional
from config.settings import config
from utils.logger import logger

class APIClient:
    def __init__(self):
        self.quotes_cache = {}
        self.cache_timeout = 300  # 5 минут
        
        # резервные цитаты на случай недоступности API
        self.backup_quotes = [
            "Успех - это способность идти от одной неудачи к другой, не теряя энтузиазма. - Уинстон Черчилль",
            "Единственный способ делать отличную работу - любить то, что вы делаете. - Стив Джобс", 
            "Будущее принадлежит тем, кто верит в красоту своих мечей. - Элеонора Рузвельт",
            "Не ждите. Время никогда не будет подходящим. - Наполеон Хилл",
            "Путешествие в тысячу миль начинается с одного шага. - Лао-цзы",
            "Делайте что можете, с тем что у вас есть, там где вы находитесь. - Теодор Рузвельт"
        ]
    
    async def get_quote(self) -> Optional[str]:
        """получение цитаты дня с кэшированием"""
        cache_key = "daily_quote"
        
        # проверка кэша
        if cache_key in self.quotes_cache:
            cached_quote, timestamp = self.quotes_cache[cache_key]
            if asyncio.get_event_loop().time() - timestamp < self.cache_timeout:
                return cached_quote
        
        try:
            timeout = aiohttp.ClientTimeout(total=5)  # уменьшил таймаут до 5 сек
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(config.quotes_api_url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        quote = f"{data['content']} - {data['author']}"
                        # кэширование результата  
                        self.quotes_cache[cache_key] = (quote, asyncio.get_event_loop().time())
                        logger.info("получена новая цитата")
                        return quote
        except asyncio.TimeoutError:
            logger.warning("таймаут при запросе цитаты, использую резервную")
        except Exception as e:
            logger.warning(f"ошибка получения цитаты: {e}, использую резервную")
        
        # возвращаем случайную резервную цитату
        backup_quote = random.choice(self.backup_quotes)
        logger.info("использована резервная цитата")
        return backup_quote

api_client = APIClient()