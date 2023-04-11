import datetime
import aiohttp
import requests
import asyncio
import environ
from aiohttp import ClientSession

from db_work import save_database

env = environ.Env()
environ.Env.read_env()


URL = env('url_swapi')


async def get_total_size():
    async with ClientSession() as client:
        data = await client.get(URL, ssl=False)
        response = await data.json()
        all_persons_num = response['count']
        return all_persons_num


async def get_character(url: str):
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            return await response.json()


def data_generate(url_list):
    try:
        for url in url_list:
            result = requests.get(url)
            yield result.json()['name']
    except KeyError:
        for url in url_list:
            result = requests.get(url)
            yield result.json()['title']


async def get_planet(url: str):
    async with aiohttp.client.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            return await response.json()


async def get_persons():
    swapi_all_list = list()
    total_count = await get_total_size()

    characters_tasks = [get_character(f'{URL}/{i}') for i in range(1, total_count)]
    characters_info = await asyncio.gather(*characters_tasks)
    for person in characters_info:
        try:
            data = {}
            data['birth_year'] = person['birth_year']
            data['eye_color'] = person['eye_color']
            data['films'] = ', '.join(data_generate(person['films']))
            data['gender'] = person['gender']
            data['hair_color'] = person['hair_color']
            data['height'] = person['height']
            planet = await get_planet(person['homeworld'])
            data['homeworld'] = planet['name']
            data['homeworld'] = person['homeworld']
            data['mass'] = person['mass']
            data['name'] = person['name']
            data['skin_color'] = person['skin_color']
            data['species'] = ', '.join(data_generate(person['species']))
            data['starships'] = ', '.join(data_generate(person['starships']))
            data['vehicles'] = ', '.join(data_generate(person['vehicles']))
        except:
            # ошибка с 17 персонажем выдает 404 и ломает код
            data = {}
            data['birth_year'] = '404 error'
            data['eye_color'] = '404 error'
            data['films'] = '404 error'
            data['gender'] = '404 error'
            data['hair_color'] = '404 error'
            data['height'] = '404 error'
            data['homeworld'] = '404 error'
            data['mass'] = '404 error'
            data['name'] = '404 error'
            data['skin_color'] = '404 error'
            data['species'] = '404 error'
            data['starships'] = '404 error'
            data['vehicles'] = '404 error'

        swapi_all_list.append(data)

    return list(swapi_all_list)



async def main():
    swapi_persons = await get_persons()
    await save_database(swapi_persons)


if __name__ == '__main__':
    start = datetime.datetime.now()
    asyncio.run(main())
    print(datetime.datetime.now() - start)