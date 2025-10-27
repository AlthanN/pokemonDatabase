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

import_pokemon_into_sql('all_pokemon_data.json')