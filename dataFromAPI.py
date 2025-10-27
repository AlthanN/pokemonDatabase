import requests
import json
import time

def fetch_all_pokemon_data(limit=100000):
   
    print(f"Starting to fetch {limit} Pokemon...")
    
    list_url = f"https://pokeapi.co/api/v2/pokemon/?limit={limit}&offset=0"
    
    # gets all the pokemon data
    try:
        response = requests.get(list_url)
        response.raise_for_status()
        pokemon_list = response.json()["results"]
        print(f"Found {len(pokemon_list)} Pokemon to fetch\n")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Pokemon list: {e}")
        return None
    
    all_pokemon_data = []
    failed_pokemon = []
    
    for i, pokemon in enumerate(pokemon_list, 1):
        try:
            # fetch individual Pokemon data
            response = requests.get(pokemon['url'])
            response.raise_for_status()
            data = response.json()
            
            pokemon_info = {
                "id": data["id"],
                "name": data["name"],
                "types": [type_info["type"]["name"] for type_info in data["types"]],
                "weight": data["weight"]
            }
            
            all_pokemon_data.append(pokemon_info)
            
            # progress update every 10 Pokemon
            if i % 10 == 0:
                print(f"Progress: {i}/{len(pokemon_list)} Pokemon fetched")
            
            # delay for API calls
            time.sleep(0.05)  # 50ms delay
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {pokemon['name']}: {e}")
            failed_pokemon.append(pokemon['name'])
            continue
    
    print(f"\n✓ Successfully fetched {len(all_pokemon_data)} Pokemon!")
    
    if failed_pokemon:
        print(f"✗ Failed to fetch {len(failed_pokemon)} Pokemon: {failed_pokemon}")
    
    # save to JSON file
    filename = 'all_pokemon_data.json'
    with open(filename, 'w') as f:
        json.dump(all_pokemon_data, f, indent=2)
    
    print(f"\n✓ Data saved to '{filename}'")
    print(f"File size: {len(json.dumps(all_pokemon_data)) / 1024:.2f} KB")
    
    return all_pokemon_data

# extracts data from a single pokemon
def get_pokemon_data(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        pokemon_info = {
            "id": data["id"],
            "name": data["name"],  
            "types": [type_info["type"]["name"] for type_info in data["types"]],
            "weight": data["weight"]  
        }
        
        return pokemon_info
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# executes file directly for better use, so when I import it from another file
# it doesn't run this code and only the function
if __name__ == "__main__":


    stored_pokemon = []
    
    # only use fetch_all_pokemon_data once to store all pokemon data into .json file
    # fetch_all_pokemon_data(limit=100000)

    pokemon_list = ["pikachu", "charizard", "bulbasaur", "pidgey"]
        
    with open('all_pokemon_data.json', 'r') as file:
            all_poke_data = json.load(file)
    
    for pokemon in pokemon_list:
        print(f"\nFetching data for: {pokemon}")

        for poke_data in all_poke_data:
            if poke_data['name'] == str(pokemon).lower():
                print(f"found {poke_data['name']}")
                print(f"ID: {poke_data['id']}")
                print(f"types{poke_data['types']}")
                stored_pokemon.append(poke_data)
                break

    