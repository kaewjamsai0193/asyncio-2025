import time
import asyncio, httpx, json
student_id = "6620301002"

async def fire_rocket(name: str, t0: float):
    url = f"http://172.16.2.117:8088/fire/{student_id}"
    start_time = time.perf_counter() - t0  # เวลาเริ่มสัมพัทธ์
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        data = r.json()
        time_to_target = data.get("time_to_target")
        end_time = time.perf_counter() - t0
        return {
            "name": name,
            "start_time": start_time,
            "time_to_target": time_to_target,
            "end_time": end_time
        }

    """
    TODO:
    - ส่ง GET request ไปยัง rocketapp ที่ path /fire/{student_id}
    - อ่านค่า time_to_target จาก response
    - return dict ที่มี:
        {
            "name": name,
            "start_time": start_time,
            "time_to_target": time_to_target,
            "end_time": end_time
        }
    """
    pass

async def main():
    t0 = time.perf_counter()  # เวลาเริ่มของชุด rockets

    print("Rocket prepare to launch ...")  # แสดงตอนเริ่ม main

    # TODO: สร้าง task ยิง rocket 3 ลูกพร้อมกัน
    tasks = []
    for i in range(1,4):
        tasks.append(asyncio.create_task(fire_rocket(i, t0)))

    # TODO: รอให้ทุก task เสร็จและเก็บผลลัพธ์ตามลำดับ task
    results = await asyncio.gather(*tasks)

    # TODO: แสดงผล start_time, time_to_target, end_time ของแต่ละ rocket ตามลำดับ task
    print("Rockets fired:")
    for r in results:
        print(
            f"Rocket-{r['name']} | "
            f"start_time: {r['start_time']:.2f} sec | "
            f"time_to_target: {r['time_to_target']:.2f} sec | "
            f"end_time: {r['end_time']:.2f} sec"
        )
    pass  # แสดงผล rocket

    # TODO: แสดงเวลารวมทั้งหมดตั้งแต่ยิงลูกแรกจนลูกสุดท้ายถึงจุดหมาย
    t_total = max(r["end_time"] for r in results)
    print(f"\nTotal time for all rockets: {t_total:.2f} sec")

asyncio.run(main())