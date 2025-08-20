import asyncio

async def task(value):
    await asyncio.sleep(1)
    return value * 100

async def main():
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(task(i)) for i in range(1,10)]
    for t in tasks:
        print(f'{t.result()}')

asyncio.run(main())