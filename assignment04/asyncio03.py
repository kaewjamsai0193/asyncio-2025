# Create 2 Tasks with High-Level API\
import asyncio

async def dowload_image(name, delay):
    print(f"{name} กำลังโหลด...")
    await asyncio.sleep(delay)
    print(f"{name} โหลดเสร็จแล้ว!")

async def main():
    task1 = asyncio.create_task(dowload_image("ภาพที่ 1 ", 2))
    task2 = asyncio.create_task(dowload_image("ภาพที่ 2 ", 3))

    await task1
    await task2

asyncio.run(main())
