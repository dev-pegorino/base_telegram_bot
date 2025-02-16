from sqlalchemy import ForeignKey, BigInteger, Integer, String, DateTime
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from datetime import datetime

from config import DATABASE_URL


engine = create_async_engine(url=DATABASE_URL, echo=False)

async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger())
    lang: Mapped[str] = mapped_column(String(2), default='en')
    role: Mapped[str] = mapped_column(String(), default='user')


class SubChannel(Base):
    __tablename__ = 'sub_channels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    type: Mapped[str] = mapped_column(String(), default='Channel')
    username: Mapped[str] = mapped_column(String(32))
    

class CaptchaAttempts(Base):
    __tablename__ = 'captcha_attempts'
    
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(BigInteger, unique=True)
    attempts_left = mapped_column(Integer, default=3)
    blocked_until = mapped_column(DateTime, nullable=True)
    
    def is_blocked(self) -> bool:
        if self.blocked_until is None:
            return False
        return datetime.now() < self.blocked_until


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)