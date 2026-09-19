import pandas as pd
import psycopg2
conn = psycopg2.connect(
    dbname="agrobio_db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

df = pd.read_sql("SELECT cultivo, rendimiento FROM cultivos", conn)
print(df)

cur.close()
conn.close()