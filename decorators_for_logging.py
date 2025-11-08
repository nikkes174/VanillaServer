import asyncio
import functools
import itertools
import time

event = asyncio.Event()
counter = itertools.count(1)


def logger_for_request(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        counter_id = next(counter)
        print(f'Начало запроса [{counter_id}] {func.__name__}')
        start = time.monotonic()

        result = await func(*args, **kwargs)

        end = time.monotonic() - start
        print(f'Конец запроса [{counter_id}] {func.__name__} за {end:.2f} сек')
        return result

    return wrapper


def group_logger(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = await func(*args, **kwargs)
        end = time.monotonic() - start
        event.set()
        print(f'{len(result)} для клиента выполнено за {end:.2f} сек')
        event.clear()
        return result

    return wrapper
