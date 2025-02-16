from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

import app.database.requests as rq
from app.utils.strings import get_text
import app.utils.keyboards as kb
import app.utils.functions as func
from app.handlers.users.commands import user_captcha

from datetime import datetime


router = Router()


@router.callback_query(F.data.startswith('captcha_'))
async def process_captcha(call: CallbackQuery):
    lang = call.from_user.language_code
    user_id = call.from_user.id
    _, answer = call.data.split('_')
    answer = int(answer)
    
    attempts = await rq.get_captcha_attempts(user_id)
    if attempts.is_blocked():
        remaining_time = attempts.blocked_until - datetime.now()
        minutes = remaining_time.seconds // 60
        await call.answer(
            get_text("captcha_blocked", lang).format(minutes=minutes),
            show_alert=True
        )
        return
    
    correct_answer = user_captcha[user_id]
    
    if answer == correct_answer:
        await rq.reset_captcha_attempts(user_id)
        await call.message.edit_text(
                get_text("captcha_correct", lang),
                reply_markup=await kb.language_keyboard(lang)
            )
    else:
        attempts_left, blocked_until = await rq.decrease_captcha_attempts(user_id)
        if blocked_until:
            await call.answer(
                get_text("captcha_blocked_all", lang),
                show_alert=True
            )
        else:
            problem, answer = func.generate_math_captcha()
            user_captcha[user_id] = answer
            await call.message.edit_text(
                get_text("captcha_incorrect", lang).format(problem=problem),
                reply_markup=await kb.captcha_keyboard(answer)
            )
            await call.answer(
                get_text("captcha_wrong", lang).format(attempts_left=attempts_left),
                show_alert=True
            )


@router.callback_query(F.data.startswith('language_'))
async def process_language(call: CallbackQuery, bot: Bot):
    lang = call.data.split('_')[1]
    user_id = call.from_user.id

    await rq.create_user(user_id, lang=lang)
    await call.message.edit_text(get_text("language_selected", lang).format(lang=lang))
    await call.answer()