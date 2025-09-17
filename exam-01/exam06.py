# Hint:
# ปัญหา: asyncio.gather() จะ throw ข้อผิดพลาดทั้งหมด ไม่ใช่แค่ตัวแรก
# ให้แก้ไขโค้ดเพื่อให้สามารถ จัดการข้อผิดพลาดแยกแต่ละ task ได้
# Result:
# [ValueError('Something went wrong!'), ValueError('Something went wrong!')]

import asyncio

async def risky_task():
    raise ValueError("Something went wrong!")

async def main():
    try:
        await asyncio.gather(risky_task(), risky_task())

    except Exception as e:
        print([e for _ in range(2)])
asyncio.run(main())
