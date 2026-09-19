import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    dbname="agrobio_db", user="postgres",
    password="1234", host="localhost", port="5432"
)

df_rend = pd.read_sql(
    "SELECT cultivo, AVG(rendimiento) AS rendimiento "
    "FROM cultivos GROUP BY cultivo ORDER BY rendimiento DESC",
    conn
)

df_rend.plot(kind='bar', x='cultivo', y='rendimiento',
             title='Rendimiento por cultivo', legend=False)
plt.ylabel('Rendimiento promedio (t/ha)')
plt.xlabel('Cultivo')
plt.xticks(rotation=45)
plt.tight_layout()

df_prod = pd.read_sql(
    "SELECT anio, SUM(produccion) AS produccion "
    "FROM cultivos GROUP BY anio ORDER BY anio",
    conn
)
conn.close()

df_prod.plot(kind='line', x='anio', y='produccion', marker='o',
             title='Producción total por año', legend=False)
plt.ylabel('Producción total (t)')
plt.xlabel('Año')
plt.xticks(df_prod['anio'])
plt.tight_layout()
plt.show()