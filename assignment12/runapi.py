# runapi_sequential.py
import asyncio, httpx, json

SERVERS = [
    "http://172.20.49.87:8000",
    "http://172.20.50.15:8000",
    "http://172.20.50.30:8000"  # ตัวอย่าง server ที่ 3
]

ENDPOINTS = ["/students", "/analytics/group", "/analytics/enrolled_year"]

async def fetch(client, base_url, endpoint):
    try:
        r = await client.get(f"{base_url}{endpoint}")
        r.raise_for_status()
        return endpoint, r.json()
    except Exception as e:
        return endpoint, {"error": str(e)}

async def fetch_server(server, endpoint):
    async with httpx.AsyncClient() as client:
        ep, data = await fetch(client, server, endpoint)

    output = {"server": server}

    # จัดรูปแบบตาม endpoint
    if ep == "/students" and isinstance(data, list):
        output["student_count"] = len(data)
    elif ep == "/analytics/group":
        output["group_analytics"] = data
    elif ep == "/analytics/enrolled_year":
        output["year_analytics"] = data
    else:
        output["result"] = data  # fallback เผื่อ error

    print(json.dumps(output, indent=2, ensure_ascii=False))

async def main():
    tasks = [fetch_server(s, e) for s, e in zip(SERVERS, ENDPOINTS)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
