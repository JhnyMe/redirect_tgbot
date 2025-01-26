import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import tags, get_and_send_post

async def main():
    logging.basicConfig(level=logging.INFO)
    # Объект бота
    bot = Bot(token="7286889495:AAEQ2aEGh-B6Y89QR2R2M9VIFeJqRzwX-qc")
    # Диспетчер
    dp = Dispatcher()

    dp.include_routers(tags.router, get_and_send_post.router)

    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())