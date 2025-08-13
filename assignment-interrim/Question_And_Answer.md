# Question
1. ถ้าสร้าง asyncio.create_task(*tasks) ที่ไม่มี await ที่ main() เกิดอะไรบ้าง
   1. Task จะเริ่มรันทันทีใน background หลังจากถูกสร้าง (เมื่อ event loop ว่างพอ)
   2. ถ้า main() จบก่อน task เสร็จ -> event loop จะปิด และ task ที่เหลือจะถูกยกเลิก (CancelledError) หรือไม่รันต่อเลย
   3. ไม่มีการจัดการ error -> ถ้า task เกิด exception และไม่มี await หรือ callback ไปดึง จะเกิด warning "Task exception was never retrieved"
2. ความแตกต่างระหว่าง asyncio.gather(*tasks) กับ asyncio.wait(tasks) คืออะไร
   1. gather -> รอให้ครบทุกอัน, คืนผลลัพธ์เป็น list ตามลำดับ
   2. wait -> คืน (done, pending) และเลือกหยุดเมื่อครบเงื่อนไข (FIRST_COMPLETED หรืออื่นๆ)
   3. gather เหมาะกับเอาผลทุกอัน, wait เหมาะกับดักผลทีละส่วน
3. สร้าง create_task() และ coroutine ของ http ให้อะไรต่างกัน
   1. create_task() -> เริ่มทำงานทันทีใน background (พร้อมกับงานอื่นได้ไม่ต้องรอ await)
   2. coroutine -> แค่เตรียมงาน ยังไม่เริ่มทำ จนกว่าจะ await
   3. await get_http() = รอให้เสร็จก่อนค่อยทำต่อ, asyncio.create_task(get_http()) = สั่งให้ทำไปพร้อมๆ กัน
