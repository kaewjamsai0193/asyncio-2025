# example of starting many tasks and getting access to all tasks
import time
import asyncio


async def dowload_image(name, delay):
    print(f"{time.ctime()} {name} กำหลังโหลด...")
    await asyncio.sleep(delay)
    print(f"{time.ctime()} {name} โหลดเสร็จแล้ว!")

async def main():
    print(f"{time.ctime()} main coroutine started")
    delays = {2: 0, 1: 1, 0: 2}
    started_tasks = [asyncio.create_task(dowload_image(i, j)) for i,j in zip(range(3),reversed(range(3)))]

    await asyncio.sleep(0.1)
    for task in started_tasks:
        await task
asyncio.run(main())

