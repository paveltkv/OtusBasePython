"""
создайте алхимичный engine
добавьте declarative base (свяжите с engine)
создайте объект Session
добавьте модели User и Post, объявите поля:
для модели User обязательными являются name, username, email
для модели Post обязательными являются user_id, title, body
создайте связи relationship между моделями: User.posts и Post.user
"""

import os

from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, scoped_session, declared_attr
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

SQLA_ASYNC_CONN_URI = "sqlite+aiosqlite:///database.db"
SQLA_ECHO = True


class Base:

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        return str(self)


engine = create_async_engine(
    SQLA_ASYNC_CONN_URI,
    echo=SQLA_ECHO,
)

Session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base(bind=engine, cls=Base)


class User(Base):
    name = Column(String(128), nullable=False)
    username = Column(String(32), unique=True, nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    posts = relationship("Post", back_populates="user")


class Post(Base):
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=False, index=True,)
    title = Column(String(200), nullable=False, default="", server_default="",)
    body = Column(Text, nullable=False, default="", server_default="",)
    user = relationship("User", back_populates="posts")


async def create_schemas():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
