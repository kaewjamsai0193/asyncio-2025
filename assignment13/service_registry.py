from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# โครงสร้างข้อมูลสำหรับเก็บบริการที่ลงทะเบียน
services_registry: Dict[str, dict] = {}

class Service(BaseModel):
    name: str
    url: str
    city: str
@app.get("/services")
async def get_services():
    """ดึงข้อมูลบริการทั้งหมดที่ลงทะเบียน"""
    return services_registry

@app.post("/register")
async def register_service(service: Service):
    """ลงทะเบียนบริการใหม่"""
    if service.name in services_registry:
        raise HTTPException(status_code=400, detail="Service already registered")
    services_registry[service.name] = service.dict()
    return {"message": "Service registered successfully"}

@app.put("/update")
async def update_service(service: Service):
    """อัปเดตข้อมูลบริการ"""
    if service.name not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    services_registry[service.name] = service.dict()
    return {"message": "Service updated successfully"}

@app.delete("/unregister/{name}")
async def unregister_service(name: str):
    """ยกเลิกการลงทะเบียนบริการตามชื่อ"""
    if name not in services_registry:
        raise HTTPException(status_code=404, detail="Service not found")
    del services_registry[name]
    return {"message": "Service unregistered successfully"}