from aiogram import BaseMiddleware

class DbMiddleware(BaseMiddleware):
    def __init__(self, pool):
        self.pool = pool

    async def __call__(self, handler, event, data):
        data["db"] = self.pool
        return await handler(event, data)