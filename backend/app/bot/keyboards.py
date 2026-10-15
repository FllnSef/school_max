from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_start_keyboard(webapp_url: str) -> InlineKeyboardMarkup:
    """Инлайн-кнопка для запуска Telegram WebApp прямо внутри чата"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🏫 Открыть Школа.MAX (WebApp)",
                    web_app=WebAppInfo(url=webapp_url)
                )
            ]
        ]
    )

def get_main_reply_keyboard(webapp_url: str) -> ReplyKeyboardMarkup:
    """Нижняя кнопка клавиатуры для быстрого доступа"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🚀 Открыть экосистему",
                    web_app=WebAppInfo(url=webapp_url)
                )
            ],
            [
                KeyboardButton(text="ℹ️ Помощь"),
                KeyboardButton(text="⏰ Мои дедлайны")
            ]
        ],
        resize_keyboard=True
    )
