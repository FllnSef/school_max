from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from keyboards import get_start_keyboard, get_main_reply_keyboard

router = Router()

# Вставьте адрес вашего сайта (например, локальный через ngrok или реальный домен)
WEBAPP_URL = " https://fbngz-176-110-191-208.free.pinggy.net"

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Приветственное сообщение при старте бота"""
    inline_kb = get_start_keyboard(WEBAPP_URL)
    reply_kb = get_main_reply_keyboard(WEBAPP_URL)
    
    await message.answer(
        f"Здравствуйте, **{message.from_user.first_name}**! 👋\n\n"
        "Добро пожаловать в единую цифровую экосистему **«Школа.MAX»**.\n\n"
        "📱 Нажмите на кнопку ниже, чтобы открыть расписание, задачи, меню столовой и личный кабинет прямо внутри Telegram:",
        reply_markup=inline_kb,
        parse_mode="Markdown"
    )
    
    # Также отправляем нижнюю кнопку для удобства
    await message.answer("Или используйте кнопку в меню ниже ⬇️", reply_markup=reply_kb)

@router.message(F.text == "ℹ️ Помощь")
@router.message(Command("help"))
async def help_handler(message: Message):
    """Справка по боту"""
    await message.answer(
        "ℹ️ **Справка Школа.MAX**\n\n"
        "• **WebApp:** Все сервисы школы объединены в одном мини-приложении.\n"
        "• **Уведомления:** Бот автоматически напоминает о сдаче лабораторных и контрольных работ.\n"
        "• **Питание:** Запись на обед в столовой в 1 клик.\n\n"
        "Разработано для Всероссийского хакатона «Идея фикс».",
        parse_mode="Markdown"
    )

@router.message(F.text == "⏰ Мои дедлайны")
async def deadlines_handler(message: Message):
    """Быстрый просмотр срочных задач"""
    await message.answer(
        "⏰ **Ближайшие дедлайны:**\n\n"
        "1. 🧪 **Физика:** Лабораторная работа №2 — *до 25 сентября*\n"
        "2. 💻 **Информатика:** Практическая по HTML — *до 28 сентября*\n\n"
        "Подробный отчет доступен внутри WebApp!",
        parse_mode="Markdown"
    )
