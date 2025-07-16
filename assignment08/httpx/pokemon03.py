import asyncio
import httpx

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://pokeapi.co/api/v2/pokemon/pikachu')
        data = response.json()
        print(f"Name: {data['name']}")
        print(f"Id: {data['id']}")
        print(f"Height: {data['height']}")
        print(f"Weight: {data['weight']}")
        print(f"Type: {data['types'][0]['type']['name']}")

asyncio.run(main())