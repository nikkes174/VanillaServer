import asyncio

import aiohttp
from aiohttp import web

from decorators_for_logging import group_logger, logger_for_request

semaphore = asyncio.Semaphore(5)


@logger_for_request
async def fetch_random_dog(session):
    async with semaphore:
        async with session.get(
            'https://dog.ceo/api/breeds/image/random'
        ) as resp:
            await asyncio.sleep(0.5)
            data = await resp.json()
            return data['message']


@logger_for_request
async def fetch_random_cat(session):
    async with semaphore:
        async with session.get(
            "https://api.thecatapi.com/v1/images/search"
        ) as resp:
            await asyncio.sleep(0.5)
            data = await resp.json()
            return data[0]['url']


@group_logger
async def fetch_all_animals(count: int):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_random_dog(session) for _ in range(count)] + [
            fetch_random_cat(session) for _ in range(count)
        ]

        result = await asyncio.gather(*tasks)
        return result


async def handle(request):
    count = int(request.query.get('count', 3))
    lst_tasks = await fetch_all_animals(count)
    return web.json_response(lst_tasks)


async def init_app():
    app = web.Application()
    app.router.add_get('/animals', handle)
    return app


def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = loop.run_until_complete(init_app())
    web.run_app(app, port=8080)


if __name__ == "__main__":
    main()
