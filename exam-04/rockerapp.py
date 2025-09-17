import asyncio
import random
from fastapi import FastAPI, HTTPException

app = FastAPI()


async def launch_rocket(student_id: str, time_to_target: float):
    # log ตอนเริ่ม
    print(f"Rocket {student_id} launched! ETA: {time_to_target:.2f} seconds")
    await asyncio.sleep(time_to_target)
    # log ตอนถึง
    print(f"Rocket {student_id} reached destination after {time_to_target:.2f} seconds")


@app.get("/fire/{student_id}")
async def fire_rocket(student_id: str):
    # ตรวจสอบว่า student_id ต้องเป็นตัวเลข 10 หลัก
    if not (student_id.isdigit() and len(student_id) == 10):
        raise HTTPException(status_code=400, detail="Invalid student_id. Must be 10 digits.")

    # random เวลา 1–2 วินาที
    time_to_target = round(random.uniform(1, 2), 2)

    # สร้าง background task
    task = asyncio.create_task(launch_rocket(student_id, time_to_target))

    # ส่ง response กลับทันที
    return {
        "message": f"Rocket {student_id} fired!",
        "time_to_target": time_to_target
    }
