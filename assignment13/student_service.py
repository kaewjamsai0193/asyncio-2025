from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import httpx, os
from dotenv import load_dotenv
import folium
# โหลดค่า .env
load_dotenv(".env")

API_KEY = os.getenv("OWM_API_KEY")
DEFAULT_CITY = os.getenv("CITY")
SERVICE_REGISTRY_URL = os.getenv("SERVICE_REGISTRY_URL")
STUDENT_NAME = os.getenv("STUDENT_NAME")
SELF_URL = os.getenv("SELF_URL")

app = FastAPI()

@app.get("/weather", response_class=HTMLResponse)
async def weather_map(city: str = DEFAULT_CITY):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="❌ Missing OWM_API_KEY in .env")

    # ดึงข้อมูลสภาพอากาศจาก OpenWeatherMap
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "th"}

    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, params=params)

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    data = resp.json()
    lat = data.get("coord", {}).get("lat")
    lon = data.get("coord", {}).get("lon")
    temp = data.get("main", {}).get("temp")
    humidity = data.get("main", {}).get("humidity")
    weather_desc = data.get("weather", [{}])[0].get("description")

    # สร้าง Folium map
    m = folium.Map(location=[lat, lon], zoom_start=10)

    # Marker แสดงข้อมูลสภาพอากาศ
    popup_text = f"{city} <br>Temp: {temp}°C <br>Humidity: {humidity}% <br>Weather: {weather_desc}"
    folium.Marker([lat, lon], popup=popup_text, tooltip=city).add_to(m)

    # Circle แสดงอุณหภูมิ (ขนาด proportional)
    folium.Circle(
        location=[lat, lon],
        color="red",
        fill=True,
        fill_opacity=0.3,
        popup=f"Temp: {temp}°C"
    ).add_to(m)
    # คืนค่า HTML ให้ browser แสดง map interactive
    return m._repr_html_()

@app.get("/aggregate", response_class=HTMLResponse)
async def aggregate_map(format: str = "html"):
    """
    ดึง weather จากทุก service แล้วสร้างแผนที่ Folium รวม
    - format=html → คืนค่า Folium map
    - format=json → คืนค่า JSON ของทุกเมือง
    """
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(f"{SERVICE_REGISTRY_URL}/services")
            response.raise_for_status()
            services = response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Service Registry Error: {e}")

        results = []
        # สร้าง map หนึ่งครั้งตรงกลางประเทศไทย
        m = folium.Map(location=[13.75, 100.5], zoom_start=6)
        added = False

        for service_name, service in services.items():
            city = service.get("city", service_name)
            try:
                owm_url = "https://api.openweathermap.org/data/2.5/weather"
                params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "th"}
                r = await client.get(owm_url, params=params)
                r.raise_for_status()
                data = r.json()

                lat = data.get("coord", {}).get("lat")
                lon = data.get("coord", {}).get("lon")
                temp = data.get("main", {}).get("temp")
                humidity = data.get("main", {}).get("humidity")
                weather_desc = data.get("weather", [{}])[0].get("description")

                results.append({
                    "service": service_name,
                    "city": city,
                    "lat": lat,
                    "lon": lon,
                    "temperature": temp,
                    "humidity": humidity,
                    "description": weather_desc
                })

                # ใส่ marker ลง map
                if lat and lon:
                    popup_text = f"{city} <br>Temp: {temp}°C <br>Humidity: {humidity}% <br>Weather: {weather_desc}"
                    folium.Marker([lat, lon], popup=popup_text, tooltip=city).add_to(m)
                    folium.Circle(
                        location=[lat, lon],
                        color="red",
                        fill=True,
                        fill_opacity=0.3,
                        popup=f"Temp: {temp}°C"
                    ).add_to(m)
                    added = True
            except Exception as e:
                print(f"Error fetching weather for {city}: {e}")

        if not added:
            folium.Marker(
                location=[13.75, 100.5],
                popup="No weather data found",
                icon=folium.Icon(color="red", icon="exclamation-sign")
            ).add_to(m)

        if format == "json":
            return results
        else:
            return m.get_root().render()





@app.post("/register")
async def register_self():
    service_info = {
        "name": STUDENT_NAME,
        "url": SELF_URL,
        "city": DEFAULT_CITY
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICE_REGISTRY_URL}/register", json=service_info)
        return response.json()

@app.put("/update_self")
async def update_self():
    service_info = {
        "name": STUDENT_NAME,
        "url": SELF_URL,
        "city": DEFAULT_CITY
    }
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{SERVICE_REGISTRY_URL}/update", json=service_info)
        return response.json()

@app.delete("/unregister_self")
async def unregister_self():
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{SERVICE_REGISTRY_URL}/unregister/{STUDENT_NAME}")
        return response.json()