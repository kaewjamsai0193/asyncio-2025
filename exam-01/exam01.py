# Hint:
# ให้หาข้อผิดพลาดและแก้ไขโค้ดให้ทำงานถูกต้อง
# Result:
# Hello
# World

import asyncio

async def say_hello():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

async def main():
    await say_hello()

asyncio.run(main())

