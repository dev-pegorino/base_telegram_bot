from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

import app.database.requests as rq
from app.utils.strings import get_text
import app.utils.keyboards as kb
import app.utils.functions as func


router = Router()

user_captcha = {}


@router.message(CommandStart(), func.IsFollower())
async def start(message: Message, bot: Bot, state: FSMContext):
    await state.clear()

    user_id = message.from_user.id
    user = await rq.get_user(user_id)
    lang = message.from_user.language_code

    if user is None:    
        problem, answer = func.generate_math_captcha()
        user_captcha[user_id] = answer
            
        await message.answer(
            get_text("captcha", lang).format(problem=problem),
            reply_markup=await kb.captcha_keyboard(answer)
        )
    else:
        await message.answer(get_text("start", user.lang))


@router.message(~func.IsFollower())
async def start_no_followers(message: Message):
    user_id = message.from_user.id
    user = await rq.get_user(user_id)
    lang = message.from_user.language_code

    if user is None:
        await message.answer(get_text("no_sub_channels", lang), reply_markup=await kb.sub_channels_keyboard(lang))
    else:
        await message.answer(get_text("no_sub_channels", user.lang), reply_markup=await kb.sub_channels_keyboard(user.lang))


@router.message(F.text)
async def message(message: Message):
    user_id = message.from_user.id
    user = await rq.get_user(user_id)

    if user is None:
        lang = message.from_user.language_code
        return await message.answer(get_text("dont_understand", lang))
    await message.answer(get_text("dont_understand", user.lang))