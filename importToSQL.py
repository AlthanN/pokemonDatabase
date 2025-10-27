import pyodbc as odbc
import json
import os
from dotenv import load_dotenv

load_dotenv()

DRIVER_NAME = os.getenv('DRIVER_NAME')
SERVER_NAME = os.getenv('SERVER_NAME')
DATABASE_NAME = os.getenv('DATABASE_NAME')

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""

def import_pokemon_into_sql(pokemon_json):
    with open(pokemon_json, 'r') as file:
        pokemon_data = json.load(file)
    print(f'found {len(pokemon_data)} pokemon to import!')

    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    print(cursor.connection)
    # creates table if it doesn't exist
    try:
        cursor.execute('''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='pokemon' AND xtype='U')
        CREATE TABLE pokemon (
            id INT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            types VARCHAR(100),
            weight INT
        )
        ''')
        conn.commit()
    except:
        print("table could not be created")

    try:
        for pokemon in pokemon_data:
            types_str = ','.join(pokemon['types'])
            cursor.execute('SELECT id FROM pokemon WHERE id = ?', (pokemon['id'],))
            exists = cursor.fetchone()

            #Update our current data of the pokemon if it exists
            if exists:
                cursor.execute('' \
                    'UPDATE pokemonDB' \
                    'SET name = ?,' \
                        'types = ?,' \
                        'weight = ?,' \
                    'WHERE id = ?',
                (pokemon['name'], types_str, pokemon['weight'], pokemon['id']))
            else: 
                #Import current data of pokemon
                cursor.execute('''
                INSERT INTO pokemon (id, name, types, weight)
                VALUES (?, ?, ?, ?)
                ''', (pokemon['id'], pokemon['name'], types_str, pokemon['weight']))
    except:
        print(f"could not import into SQL")
        
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Successfully imported {len(pokemon_data)} Pokemon!")

if __name__ == "__main__":
    import_pokemon_into_sql('all_pokemon_data.json')