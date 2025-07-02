# example of waiting for all tasks to complete
from random import random
import asyncio

async def task_coro(arg):
    value = random()
    await asyncio.sleep(value)
    print(f'>task {arg} done with {value}')

async def main():
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]

    done, pendinf = await asyncio.wait(tasks)

    print('All done')

asyncio.run(main())
