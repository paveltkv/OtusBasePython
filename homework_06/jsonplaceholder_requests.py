from dataclasses import dataclass

from aiohttp import ClientSession, ClientResponse
import asyncio

USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(session: ClientSession, url: str) -> dict:
    async with session.get(url) as response:  # type: ClientResponse
        response_json = await response.json()
        return response_json


async def fetch_users_data() -> list[dict]:
    async with ClientSession() as session:
        data = await fetch_json(session, USERS_DATA_URL)
    return [{'id': item['id'], 'name': item['name'], 'username': item['username'], 'email': item['email']} for item in data]


async def fetch_posts_data() -> list[dict]:
    async with ClientSession() as session:
        data = await fetch_json(session, POSTS_DATA_URL)
    return [{'id': item['id'], 'userId': item['userId'], 'title': item['title'], 'body': item['body']} for item in data]


async def get_data():
    return await asyncio.gather(
        fetch_users_data(),
        fetch_posts_data(),
    )
