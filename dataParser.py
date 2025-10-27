import json

with open("all_pokemon_data.json", 'r') as file:
    pokemon_data = json.load(file)

inp = input("What kind of type would you like to find for pokemon? ")
inp = inp.lower()

    
if pokemon_data:
    print("\n" + "="*50)
    print("EXAMPLES OF USAGE:")
    print("="*50)
        
    # Example 1: Get all flying types
    flying_pokemon = [p for p in pokemon_data if inp in p['types']]
    print(f"\nFlying-type Pokemon ({len(flying_pokemon)}):")
    for p in flying_pokemon[:5]:  # Show first 5
        print(f"  - {p['name'].capitalize()}: {p['types']}")
        
    # Example 2: Get heaviest Pokemon
    heaviest = max(pokemon_data, key=lambda p: p['weight'])
    print(f"\nHeaviest Pokemon: {heaviest['name'].capitalize()} ({heaviest['weight']/10} kg)")
        
    # Example 3: Count by type
    type_counts = {}
    for p in pokemon_data:
        for t in p['types']:
            type_counts[t] = type_counts.get(t, 0) + 1
        
    print(f"\nMost common types:")
    sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
    for type_name, count in sorted_types[:5]:
        print(f"  - {type_name.capitalize()}: {count} Pokemon")