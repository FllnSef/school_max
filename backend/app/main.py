from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from contextlib import asynccontextmanager
import os

from app.database import engine, Base
import app.models.task
import app.models.user

# Импорт роутеров
from app.routers import auth, schedule, tasks, menu, ai

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Автоматическое создание всех таблиц в SQLite при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Школа.MAX API",
    description="Бэкенд интеграции сервисов Сферум и MAX",
    version="1.0.0",
    lifespan=lifespan
)

# Разрешаем CORS для запросов из браузера
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение всех роутеров API
app.include_router(auth.router)
app.include_router(schedule.router)
app.include_router(tasks.router)
app.include_router(menu.router)
app.include_router(ai.router)

# Автоматический поиск и отдача index.html при открытии http://127.0.0.1:8000
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    # Проверяем возможные пути к index.html
    possible_paths = [
        os.path.join("..", "index.html"),          # Если запуск из backend/
        os.path.join("index.html"),                # В текущей папке
        os.path.join("frontend", "index.html"),    # В папке frontend/
        os.path.join("app", "static", "index.html")
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return FileResponse(path)
            
    return HTMLResponse("<h3>Фронтенд index.html не найден. Убедитесь, что он лежит в корне проекта или в папке frontend.</h3>", status_code=404)
