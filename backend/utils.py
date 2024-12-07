
import psycopg2
import os
from dotenv import load_dotenv

def connect_to_db():
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv(dotenv_path="../credendiciales.env")
    
    # Configura los parámetros de la conexión
    db_host = os.getenv("DB_HOST_AWS")
    db_username = os.getenv("DB_USER_AWS")
    db_password = os.getenv("DB_PASSWORD_AWS")
    db_database = os.getenv("DB_DATABASE_AWS")
    db_port = int(os.getenv("DB_PORT_AWS", 5432))


    print(f"DB Host: {db_host}")
    print(f"DB User: {db_username}")
    print(f"DB Password: {db_password}")
    print(f"DB Database: {db_database}")
    print(f"DB Port: {db_port}")


    print

    # Establecer la conexión
    try:
        connection = psycopg2.connect(host=db_host,
                                      database=db_database,
                                      user=db_username,
                                      password=db_password,
                                      port=db_port,
                                      sslmode="require")
        
        print("Conexión exitosa a la base de datos PostgreSQL con SSL")
        return connection  
    
    except psycopg2.OperationalError as e:
        print("Error de conexión:", e)
        return None  
    
    except Exception as error:
        print("Error desconocido:", error)
        return None  
    
connect_to_db()