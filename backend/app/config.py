import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    
    BOT_TOKEN: str
    
   
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/shkola_max.db"
    
    
    DEBUG: bool = True
    
    
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR.parent, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
