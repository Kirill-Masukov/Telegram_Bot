import asyncio
import logging
from commands import set_commands
from config import bot_token
from aiogram import Bot, Dispatcher
from handlers import router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router=router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
