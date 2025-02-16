from typing import Any, Awaitable, Callable, Dict

from aiogram.fsm.storage.redis import RedisStorage
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage) -> None:
        self.storage = storage

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
        user_id = event.from_user.id
        text = event.text
        key = f'user:{user_id}:msg:{text}'

        check_user = await self.storage.redis.get(name=key)

        if check_user:
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(name=key, value=0, ex=10)
                return await event.answer('Вы не можете отправлять одно и то же сообщение так быстро!')
            return

        await self.storage.redis.set(name=key, value=1, ex=4)
        return await handler(event, data)