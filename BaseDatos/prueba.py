import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
# Configura los parámetros de la conexión

db_host = os.getenv("DB_HOST_AWS")
db_username = os.getenv("DB_USER_AWS")
db_password = os.getenv("DB_PASSWORD_AWS")
db_database = os.getenv("DB_DATABASE_AWS")
db_port = int(os.getenv("DB_PORT_AWS", 5432))

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
        sslmode="require"
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