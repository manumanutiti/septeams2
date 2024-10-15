import pandas as pd
import sqlite3

df = pd.read_csv('team_scores.csv')
conn = sqlite3.connect('DataBase.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS team_scores_1 (
        date TEXT,
        name TEXT,
        team_work REAL,
        hard_skill REAL
    )
''')

conn.commit()
df.to_sql('team_scores_1', conn, if_exists='replace', index=False)
conn.close()
print("Tabla creada e inserción de datos realizada con éxito.")
