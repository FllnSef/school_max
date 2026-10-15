import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from handlers import router


BOT_TOKEN = "8833075656:AAFFPIP9o7XPeOt0pxxTVSDSzVLyDACWBTY"

async def main():
    token = BOT_TOKEN.strip()
    
    
    if token.startswith("ВАШ_"):
        print("\n[⚠️ ОШИБКА] Укажите ваш токен от @BotFather в файле bot_main.py!\n")
        return

    
    session = None
    session = AiohttpSession(proxy="http://185.199.229.156:7492")

    if session:
        bot = Bot(token=token, session=session)
    else:
        bot = Bot(token=token)

    dp = Dispatcher()
    dp.include_router(router)

    try:
        me = await bot.get_me()
        print(f"\n[🤖 TELEGRAM BOT] Успешное подключение! Бот: @{me.username} ({me.first_name})")
        print("[✓] Напишите боту /start в Telegram\n")
    except Exception as e:
        print(f"\n❌ Ошибка подключения к Telegram API: {e}")
        print("💡 Включите VPN на ПК и запустите снова.\n")
        if bot.session:
            await bot.session.close()
        return

    await dp.drop_pending_updates()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n[🛑 TELEGRAM BOT] Бот остановлен.")
