import requests
import json

def get_pokemon_data(pokemon_name_or_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        #Extract only the fields we want
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

#executes file directly for better use, so when I import it from another file
# it doesn't run this code and only the function
if __name__ == "__main__":
    # Fetch data for a few Pokemon
    pokemon_list = ["pikachu", "charizard", "bulbasaur", "pidgey", 25, 150]
    
    stored_pokemon = []
    
    for pokemon in pokemon_list:
        print(f"\nFetching data for: {pokemon}")
        pokemon_data = get_pokemon_data(pokemon)
        
        if pokemon_data:
            stored_pokemon.append(pokemon_data)
            print(f"ID: {pokemon_data['id']}")
            print(f"Name: {pokemon_data['name']}")
            print(f"Types: {', '.join(pokemon_data['types'])}")
            print(f"Weight: {pokemon_data['weight']} hectograms ({pokemon_data['weight']/10} kg)")
    
    #Save to JSON file
    with open('pokemon_data.json', 'w') as file: #opens/creates json file and overwrites current data
        json.dump(stored_pokemon, file, indent=2)
    #using with closes the file so we dont need to do file.close()
    print(f"\n\nStored {len(stored_pokemon)} Pokemon in pokemon_data.json")
