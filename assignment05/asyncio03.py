# example of waiting for the first task to fail
from random import random
import asyncio

async def task_coro(arg):
    value = random()
    await asyncio.sleep(value)
    print(f'>task {arg} done with {value}')
    if value < 0.1:
        raise Exception(f'Something bad happend in {arg}')

async def main():

    task = [asyncio.create_task(task_coro(i)) for i in range(10)]

    done,pending = await asyncio.wait(task,return_when=asyncio.FIRST_COMPLETED)
    print("Done")
    first = done.pop()
    print(first)

asyncio.run(main())