import asyncio
import httpx
import time
pokemon_names = ['pikachu', 'bulbasaur', 'charmander', 'squirtle', 'eevee',  'snorlax', 'gengar', 'mewtwo', 'psyduck', 'jigglypuff']

async def get_pokemon_data(name, client):
    response = await client.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
    data = response.json()
    print(f"{data['name']} -> ID : {data['id']}, Types: {[t['type']['name'] for t in data['types']]}")

async def fetch_all_pokemon(pokemon_names):
    async with httpx.AsyncClient() as client:

        tasks = [get_pokemon_data(name, client) for name in pokemon_names]

        start = time.time()
        await asyncio.gather(*tasks)
        end = time.time()
        print(f"Total time taken:{len(pokemon_names)} {end - start:.2f} seconds")


if __name__ == '__main__':
    asyncio.run(fetch_all_pokemon(pokemon_names))
