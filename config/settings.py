import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN")
    
    # api urls
    quotes_api_url: str = "https://api.quotable.io/random"
    
    # files
    tasks_file: str = "storage/tasks.json"
    log_file: str = "bot.log"
    
    def __post_init__(self):
        if not self.bot_token:
            raise ValueError("BOT_TOKEN не найден в .env файле!")

config = Settings()