import datetime
import aiohttp
import requests
import asyncio
import environ
from pprint import pprint
from aiohttp import ClientSession

from db_work import Base, People_swap, engine, Session, database_main

env = environ.Env()
environ.Env.read_env()

# env('SECRET_KEY')

URL = 'https://swapi.dev/api/people/'


async def get_total_size():
    async with ClientSession() as client:
        data = await client.get(URL, ssl=False)
        response = await data.json()
        all_persons_num = response['count']
        print(all_persons_num)
        return all_persons_num


asyncio.run(get_total_size())