import psycopg2
from psycopg2.extras import DictCursor

import os
from dotenv import load_dotenv

load_dotenv()

# Obtener las claves
db_host = os.getenv("DB_HOST_AWS")
db_username = os.getenv("DB_USER_AWS")
db_password = os.getenv("DB_PASSWORD_AWS")
db_database = os.getenv("DB_DATABASE_AWS")
db_port = int(os.getenv("DB_PORT_AWS", 5432))

# Conectar con la bbdd
conn = psycopg2.connect(database = db_database, 
                        user = db_username, 
                        host= db_host,
                        password = db_password,
                        port = db_port)

# Generamos un cursor para operar dentro de la bbdd
cur = conn.cursor()
# Comando para crear tabla de admin
cur.execute("""CREATE TABLE IF NOT EXISTS admin_data(
            admin_id SERIAL PRIMARY KEY,
            user_name VARCHAR (50) UNIQUE NOT NULL,
            password VARCHAR (24) NOT NULL);
            """)
# Grabar los cambios en la bbdd
conn.commit()
print("tabla admin creada")

# # Comando para crear tabla de preguntas
# cur.execute("""CREATE TABLE IF NOT EXISTS preguntas(
#             pregunta_id SERIAL PRIMARY KEY,
#             texto VARCHAR (200) NOT NULL);
#             """)
# # Grabar los cambios en la bbdd
# conn.commit()
# print("tabla preguntas creada")

# Comando para crear tabla de preguntas
cur.execute("""
            CREATE TABLE IF NOT EXISTS preguntas_front (
            id_categoria VARCHAR(10),  -- categoría en formato "1.1", "1.2", etc.
            titulo_categoria VARCHAR(255),
            texto_pregunta TEXT,
            texto_opcion TEXT,
            -- opcionalmente podemos generar un ID de opción único basado en la categoría
            CONSTRAINT unique_categoria_opcion UNIQUE (id_categoria, texto_pregunta, texto_opcion));
            """)
# Grabar los cambios en la bbdd
conn.commit()
print("tabla preguntas creada")

# Comando para crear tabla de usuario ¡¡¡¡¡¡¡Pendiente!!!!!!
cur.execute("""CREATE TABLE IF NOT EXISTS user_data(
            user_id SERIAL PRIMARY KEY,
            edad INTEGER NOT NULL
            );
            """)
conn.commit()
print("tabla usuario creada")


# Comando para crear tabla de sociosanitarios ¡¡¡¡¡¡¡Pendiente!!!!!!
cur.execute("""CREATE TABLE IF NOT EXISTS sociosanitarios_data(
            sociosanitario_id SERIAL PRIMARY KEY,
            ciudad VARCHAR (50) NOT NULL,
            ambito_laboral VARCHAR (50) NOT NULL,
            especialidad VARCHAR (50) NOT NULL
            );
            """)
conn.commit()
print("tabla sociosanitarios creada")

# Cerrar el cursor y la bbdd
cur.close()
conn.close()