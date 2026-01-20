import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers.user import user
from app.handlers.admin import admin
from app.database.requests import create_pool, close_pool
from app.middleware.db import DbMiddleware

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

async def on_startup(dispatcher: Dispatcher):
    pool = await create_pool(os.getenv("DATABASE_DSN"))
    dispatcher.workflow_data["db"] = pool
    dispatcher.update.middleware(DbMiddleware(pool))

async def on_shutdown(dispatcher: Dispatcher):
    pool = dispatcher.workflow_data.get("db")
    if pool:
        await close_pool(pool)

async def main():
    dp.include_router(user)
    dp.include_router(admin)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')