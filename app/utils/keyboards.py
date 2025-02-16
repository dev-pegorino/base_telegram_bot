from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.utils.strings import get_text_button
import app.database.requests as rq

import random


async def sub_channels_keyboard(lang: str="en") -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    channels = await rq.get_sub_channels()

    for channel in channels:
        keyboard.add(InlineKeyboardButton(text=f'{channel.type} {channel.name}', url=f'https://t.me/{channel.username}'))

    keyboard.add(InlineKeyboardButton(text=get_text_button("check_sub_channels", lang), callback_data=f"check_sub_channels"))
    return keyboard.adjust(1).as_markup()


async def captcha_keyboard(correct_answer: int) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    answers = [correct_answer]
    
    while len(answers) < 4:
        fake_answer = random.randint(max(0, correct_answer - 10), correct_answer + 10)
        if fake_answer != correct_answer and fake_answer not in answers:
            answers.append(fake_answer)
    random.shuffle(answers)
    
    buttons = []
    for answer in answers:
        buttons.append(InlineKeyboardButton(text=str(answer), callback_data=f"captcha_{answer}"))
    
    keyboard.add(*buttons)
    return keyboard.adjust(3).as_markup()


async def language_keyboard(lang: str="en") -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text=get_text_button("language_en", lang), callback_data=f"language_en"))
    keyboard.add(InlineKeyboardButton(text=get_text_button("language_ru", lang), callback_data=f"language_ru"))
    return keyboard.adjust(1).as_markup()