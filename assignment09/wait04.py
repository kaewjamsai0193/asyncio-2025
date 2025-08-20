from random import random
import asyncio

async def task_coro(arg):
    value = random() * 10
    await asyncio.sleep(value)
    print(f'Task {arg} done with {value}')

async def main():
    tasks = [asyncio.create_task(task_coro(i)) for i in range(10)]
    done, pending = await asyncio.wait(tasks,timeout=5)

    print(f'Done tasks: {len(done)}')
    print(f'Pending tasks: {len(pending)}')
asyncio.run(main())