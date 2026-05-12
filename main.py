import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession # Импортируем сессию
from config import TOKEN, PROXY_URL
from handlers import admin

async def main():
    # Создаем сессию с прокси
    session = AiohttpSession(proxy=PROXY_URL)
    
    # Передаем сессию боту
    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher()

    dp.include_router(admin.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close() # Чисто закрываем соединение

if __name__ == "__main__":
    asyncio.run(main())
