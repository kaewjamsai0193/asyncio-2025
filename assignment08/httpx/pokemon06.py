import asyncio, httpx

async def fetch_ability_list(limit=20):
    async with httpx.AsyncClient() as client:
        res = await client.get(f'https://pokeapi.co/api/v2/ability/?limit={limit}')
        abilities = res.json()['results']
        tasks = [client.get(url['url']) for url in abilities]
        results = await asyncio.gather(*tasks)
        return [(res.json()['name'], len(res.json()['pokemon'])) for res in results]

async def main():
    results = await fetch_ability_list()
    for name, count in results:
        print(f"{name:15} -> {count} Pokemon")

asyncio.run(main())
