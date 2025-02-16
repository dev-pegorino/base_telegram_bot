from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram import Bot

import app.database.requests as rq

import random


class IsFollower(BaseFilter):
    async def __call__(self, message: Message, bot: Bot) -> bool:
        user_id = message.from_user.id
        channels = await rq.get_sub_channels()

        if not channels:
            return False

        try:
            for channel in channels:
                member = await bot.get_chat_member(chat_id=f'@{channel.username}', user_id=user_id)
                return member.status in ['member', 'administrator', 'creator']
        except Exception as e:
            return False


def generate_math_captcha():
    operation = random.choice(['+', '-'])
    if operation == '+':
        num1 = random.randint(1, 50)
        num2 = random.randint(1, 50)
        answer = num1 + num2
        problem = f"{num1} + {num2}"
    else:
        num1 = random.randint(1, 50)
        num2 = random.randint(1, num1)
        answer = num1 - num2
        problem = f"{num1} - {num2}"
    return problem, answer