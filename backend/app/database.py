from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# Создаем асинхронный движок (Engine) базы данных
# echo=settings.DEBUG выводит все SQL-запросы в терминал при разработке
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
)

# Создаем фабрику асинхронных сессий
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Базовый класс для всех моделей данных в проекте (Declarative Base)
class Base(DeclarativeBase):
    pass

# Зависимость (Dependency Injection) для роутеров FastAPI
# Гарантирует автоматическое закрытие сессии после выполнения запроса
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
