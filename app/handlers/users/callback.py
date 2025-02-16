from aiogram import Router, F
from aiogram.types import CallbackQuery

import app.database.requests as rq
from app.utils.strings import get_text
import app.utils.keyboards as kb
import app.utils.functions as func
from app.handlers.users.commands import user_captcha


router = Router()


@router.callback_query(F.data == 'check_sub_channels', func.IsFollower())
async def start(call: CallbackQuery):
    user_id = call.from_user.id
    user = await rq.get_user(user_id)
    lang = call.from_user.language_code

    if user is None:    
        problem, answer = func.generate_math_captcha()
        user_captcha[user_id] = answer
            
        await call.message.edit_text(
            get_text("captcha", lang).format(problem=problem),
            reply_markup=await kb.captcha_keyboard(answer)
        )
    else:
        await call.message.edit_text(get_text("start", user.lang))


@router.callback_query(~func.IsFollower())
async def start_no_followers(call: CallbackQuery):
    user_id = call.from_user.id
    user = await rq.get_user(user_id)
    lang = call.from_user.language_code

    if user is None:
        await call.answer(get_text("no_sub_channels_dialog", lang), show_alert=True)
    else:
        await call.answer(get_text("no_sub_channels_dialog", user.lang), show_alert=True)
