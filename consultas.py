import psycopg2

conn = psycopg2.connect(
    dbname="agrobio_db", user="postgres",
    password="1234", host="localhost", port="5432"
)
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM cultivos")
print("Total de cultivos registrados:", cur.fetchone()[0])

cur.execute("SELECT SUM(produccion) FROM cultivos")
print("Producción total:", cur.fetchone()[0])