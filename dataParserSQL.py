import pyodbc as odbc
import pandas as pd
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
types_list = ['normal', 'water', 'grass', 'fire', 'flying', 
              'bug', 'poison', 'electric', 'ground', 'fairy',
              'fighting', 'pyschic', 'rock', 'dragon', 'steel',
              'ice', 'ghost', 'dark']
def userChoice():
    print("Welcome to a pokemon type selector, where you can search for a type of pokemon" \
    "based on their type and their weight. You can also check and see if there are any pokemon " \
    "with multiple types.")
    inpType = input("What kind of pokemon type are you looking for? ")
    inp2Type = ''
    while inpType not in types_list:
        print("please enter a valid pokemon type.")
        inpType = input("What kind of pokemon type are you looking for? ")
    
    inpChoice = input("Would you like to search for a secondary type? type yes or no ")
    if inpChoice.lower() == 'yes':
        inp2Type = input("What kind of secondary pokemon type are you looking for? ")
        
    #connect to database
    conn = odbc.connect(connection_string)
    cursor = conn.cursor()
    cursor.execute('''select * 
                from dbo.pokemon
                where types like ? and types like ?''', (f'%{inpType}%', f'%{inp2Type}%'))
    
    rows = cursor.fetchall()
    df = pd.DataFrame(rows)
    print(df)


userChoice()
