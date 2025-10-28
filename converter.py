import pandas as pd
import sqlite3

df = pd.read_csv('./output/dataset.csv')
conn = sqlite3.connect('./output/dataset.db')
df.to_sql('campaigns', conn, if_exists='replace', index=False)
conn.close()
print("Converted to SQLite!")