from random import random
import asyncio

async def task_coro(arg):
    value = random()
    await asyncio.sleep(value)
    return arg,value

async def main():
    task = [asyncio.create_task(task_coro(i)) for i in range(10)]
    done,pending = await asyncio.wait(task,return_when=asyncio.ALL_COMPLETED)
    for task in done:
        if task.done():
            print(f'Done {task.result()}')

asyncio.run(main())