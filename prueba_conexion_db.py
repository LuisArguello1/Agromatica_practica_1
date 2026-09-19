import psycopg2

conn = psycopg2.connect(
    dbname="agrobio_db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
print("Conexión exitosa")
conn.close()