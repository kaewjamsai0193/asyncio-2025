from random import random
import asyncio

async def task_coro(arg):
    value = random()
    await asyncio.sleep(value)
    print(f'Task {arg} completed with {value}')
    return arg, value

async def main():
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in done:
        if task.done():
            print(f'Done {task.result()}')
    for task in pending:
        if task.done():
            print(f'Pending  {task.result()} ')
        else:
            print(f'Pending  {task.get_name()} - {task.done()}')
asyncio.run(main())