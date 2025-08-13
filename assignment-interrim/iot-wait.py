import asyncio
import time
import random

async def get_temperature():
    await asyncio.sleep(random.uniform(0.5, 2.0))
    return f"{time.ctime()} Temp: 30°C"

async def get_humidity():
    await asyncio.sleep(random.uniform(0.5, 2.0))
    return f"{time.ctime()} Humidity: 60%"

async def get_weather_api():
    await asyncio.sleep(random.uniform(0.5, 2.0))
    return f"{time.ctime()} Weather: Sunny"

def update_dashboard(task: asyncio.Task):
    print(task.result())  # ดึงค่าจาก task ที่เสร็จแล้ว

async def main():
    start = time.time()

    tasks = [
        asyncio.create_task(get_temperature()),
        asyncio.create_task(get_humidity()),
        asyncio.create_task(get_weather_api())
    ]

    # ผูก callback ให้ทำงานเมื่อเสร็จ
    for t in tasks:
        t.add_done_callback(update_dashboard)

    await asyncio.gather(*tasks)  # รอทุกงานเสร็จ
    print(f"Took {time.time() - start:.2f} seconds")

asyncio.run(main())
