"""
Домашнее задание №3
Асинхронная работа с сетью и бд

доработайте функцию main, по вызову которой будет выполняться полный цикл программы
(добавьте туда выполнение асинхронной функции async_main):
- создание таблиц (инициализация)
- загрузка пользователей и постов
    - загрузка пользователей и постов должна выполняться конкурентно (параллельно)
      при помощи asyncio.gather (https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently)
- добавление пользователей и постов в базу данных
  (используйте полученные из запроса данные, передайте их в функцию для добавления в БД)
- закрытие соединения с БД
"""

import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine.result import Result

from jsonplaceholder_requests import get_data
from models import create_schemas, Session, User, Post


async def create_users(session: AsyncSession, users_data: list[dict]):
    for user in users_data:
        user = User(
            id=user['id'],
            name=user['name'],
            username=user['username'],
            email=user['email']
        )
        session.add(user)

    await session.commit()


async def create_posts(session: AsyncSession, posts_data: list[dict]):
    stmt = select(User)
    result: Result = await session.execute(stmt)
    users = {a1.id: a1 for a1 in result.scalars()}

    for p in posts_data:
        if p['userId'] in users:
            post = Post(
                id=p['id'],
                title=p['title'],
                body=p['body'],
                user=users[p['userId']],
            )
            session.add(post)

    await session.commit()


async def async_main():
    await create_schemas()
    users_data: list[dict]
    posts_data: list[dict]
    users_data, posts_data = await get_data()
    async with Session() as session:  # type: AsyncSession
        await create_users(session, users_data)
        await create_posts(session, posts_data)


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
