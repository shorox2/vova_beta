from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class DbMiddleware(LifetimeControllerMiddleware):
    slip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        dp_session = obj.bot.get('db')
