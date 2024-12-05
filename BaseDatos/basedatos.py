import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
# Configura los parámetros de la conexión

db_host = os.getenv("HOST")
db_username = os.getenv("AWS_USERNAME")
db_password = os.getenv("PASSWORD")
db_database = os.getenv("DATABASE")
db_port = os.getenv("PORT")

print(db_host)
print(db_username)
print(db_password)
print(db_database)
print(db_port)


# Establecer la conexión
try:
    connection = psycopg2.connect(
        host=db_host,
        database=db_database,
        user=db_username,
        password=db_password,
        port=db_port,
        sslmode='disable'
    )
    print("Conexión exitosa a la base de datos PostgreSQL con SSL")

    # Crear un cursor para interactuar con la base de datos
    cursor = connection.cursor()

    # Ejecutar una consulta de ejemplo
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("Versión de PostgreSQL:", record)

    # Cerrar cursor y conexión
    cursor.close()
    connection.close()

except psycopg2.OperationalError as e:
    print("Error de conexión:", e)
except Exception as error:
    print("Error desconocido:", error)
