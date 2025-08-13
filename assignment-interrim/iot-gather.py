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

async def main():
    start = time.time()

    coros = [get_temperature(), get_humidity(), get_weather_api()]
    results = await asyncio.gather(*coros)  # ได้ผลลัพธ์เป็น list

    for result in results:
        print(result)  # แสดงค่าที่ return ออกมา

    end = time.time()
    print(f"Took {end - start:.2f} seconds")

asyncio.run(main())
