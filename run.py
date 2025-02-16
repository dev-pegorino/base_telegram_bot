from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.handlers.users.commands import router as users_commands_router
from app.handlers.users.callback import router as users_callback_router
from app.handlers.users.reg import router as users_reg_router

from app.utils.middleware import ThrottlingMiddleware

from app.utils.commands import commands_
from app.utils.strings import settings
from config import TG_TOKEN

from app.database.models import init_db

import logging
import sys
import asyncio


logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


async def main():
    storage = RedisStorage.from_url('redis://localhost:6379/0')
    throttling_storage = RedisStorage.from_url('redis://localhost:6379/5')
    jobstores = {
        'default': RedisJobStore(
            jobs_key='dispatched_trips_jobs',
            run_times_key='dispatched_trips_running',
            db=2
        )
    }
    scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone='Europe/Moscow', jobstores=jobstores))

    bot = Bot(token=TG_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    dp.include_routers(
        users_commands_router,
        users_callback_router,
        users_reg_router,
    )
    dp.message.middleware.register(ThrottlingMiddleware(storage=throttling_storage))

    await bot.set_my_commands(commands=await commands_())
    await bot.set_my_description(settings["description"])
    await bot.set_my_short_description(settings["about"])

    await init_db()

    scheduler.ctx.add_instance(bot, declared_class=Bot)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.error("Bot stopped")
