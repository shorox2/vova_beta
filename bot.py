import asyncio
import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tg_bot.config import load_config
from aiogram import Bot, Dispatcher

from tg_bot.middlewares.db import DbMiddleware

# from tg_bot.filters.admin import AdminFilter

# from tg_bot.handlers.examples import
from tg_bot.handlers.checker import register_check_command
from tg_bot.handlers.begin import register_begin_command
from tg_bot.handlers.guides import register_guide_command
from tg_bot.handlers.marafon import register_marafoni_command


logger = logging.getLogger(__name__)

def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    # dp.filters_factory.bind(AdminFilter)
    pass

def register_all_handlers(dp):
    register_check_command(dp)
    register_begin_command(dp)
    register_guide_command(dp)
    register_marafoni_command(dp)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )
    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode= "HTML")
    storage = RedisStorage2() if config.tg_bot.user_redis else MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot Stop!")