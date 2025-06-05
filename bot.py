import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

try:
    from config.settings import config
except ValueError as e:
    print(f"❌ Ошибка конфигурации: {e}")
    print("💡 Создайте файл .env и добавьте в него: BOT_TOKEN=ваш_токен")
    exit(1)

from utils.logger import logger
from middlewares.throttling import ThrottlingMiddleware

from routers import commands
from routers.handlers import tasks, stats

async def main():
    """запуск бота"""
    # создание директории для хранения данных
    os.makedirs("storage", exist_ok=True)
    
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    dp = Dispatcher()
    
    # подключение middleware
    dp.message.middleware(ThrottlingMiddleware(rate_limit=1.0))
    
    # подключение роутеров
    dp.include_router(commands.router)
    dp.include_router(tasks.router)
    dp.include_router(stats.router)
    
    logger.info("бот запущен")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())