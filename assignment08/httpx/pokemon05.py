import asyncio
import httpx
import time
pokemon_names = ['pikachu', 'bulbasaur', 'charmander', 'squirtle', 'eevee',  'snorlax', 'gengar', 'mewtwo', 'psyduck', 'jigglypuff']

async def get_pokemon_data(name, client):
    response = await client.get(f'https://pokeapi.co/api/v2/pokemon/{name}')
    data = response.json()
    return data

async def fetch_all_pokemon(pokemon_names):
    async with httpx.AsyncClient() as client:

        tasks = [get_pokemon_data(name, client) for name in pokemon_names]

        start = time.time()
        result = await asyncio.gather(*tasks)
        sorted_result = sorted(result, key=lambda x:x['base_experience'])
        print("-------Lambda function sorted result---------")
        for i in sorted_result:
            print(f"{i['name']} -> ID : {i['id']}, Base_XP: {i['base_experience']}")
        print("\n-------Alghorithum Sort---------")
        for i in range((len(result))):
            for j in range(i + 1, len(result)):
                if result[i]['base_experience'] > result[j]['base_experience']:
                    result[i], result[j] = result[j], result[i]
        for data in result:
            print(f"{data['name']} -> ID : {data['id']}, Base_XP: {data['base_experience']}")

        end = time.time()
        print(f"Total time taken:{len(pokemon_names)} {end - start:.2f} seconds")


if __name__ == '__main__':
    asyncio.run(fetch_all_pokemon(pokemon_names))
