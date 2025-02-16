from app.database.models import User, SubChannel, CaptchaAttempts
from app.database.models import async_session
from sqlalchemy import select, update, func
from datetime import datetime, timedelta


async def get_user(user_id: int) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == user_id))
        if not user:
            return None
        return user


async def create_user(user_id: int, lang: str="en") -> User:
    async with async_session() as session:
        session.add(User(tg_id=user_id, lang=lang))
        await session.commit()


async def get_sub_channels() -> list[SubChannel]:
    async with async_session() as session:
        channels = await session.scalars(select(SubChannel))
        
        return channels if channels else []


async def get_captcha_attempts(user_id: int) -> CaptchaAttempts:
    async with async_session() as session:
        result = await session.execute(
            select(CaptchaAttempts).where(CaptchaAttempts.user_id == user_id)
        )
        attempts = result.scalar()
        if not attempts:
            attempts = CaptchaAttempts(user_id=user_id, attempts_left=3)
            session.add(attempts)
            await session.commit()
        return attempts


async def decrease_captcha_attempts(user_id: int) -> tuple[int, datetime | None]:
    async with async_session() as session:
        attempts = await get_captcha_attempts(user_id)
        attempts.attempts_left -= 1
        
        if attempts.attempts_left <= 0:
            attempts.attempts_left = 0
            attempts.blocked_until = datetime.now() + timedelta(minutes=10)
        
        session.add(attempts)
        await session.commit()
        return attempts.attempts_left, attempts.blocked_until


async def reset_captcha_attempts(user_id: int) -> None:
    async with async_session() as session:
        attempts = await get_captcha_attempts(user_id)
        attempts.attempts_left = 3
        attempts.blocked_until = None
        session.add(attempts)
        await session.commit()