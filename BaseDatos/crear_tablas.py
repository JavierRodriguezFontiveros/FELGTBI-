import psycopg2
from psycopg2.extras import DictCursor

import os
from dotenv import load_dotenv


# Conectar con la bbdd
conn = psycopg2.connect(database = , 
                        user = , 
                        host= ,
                        password = ,
                        port = 5432)

# Generamos un cursor para operar dentro de la bbdd
cur = conn.cursor()
# Comando para crear tabla de admin
cur.execute("""CREATE TABLE admin_data(
            admin_id SERIAL PRIMARY KEY,
            user_name VARCHAR (50) UNIQUE NOT NULL,
            password VARCHAR (24) NOT NULL);
            """)
# Grabar los cambios en la bbdd
conn.commit()

# Comando para crear tabla de preguntas
cur.execute("""CREATE TABLE preguntas(
            pregunta_id SERIAL PRIMARY KEY,
            texto VARCHAR (200) NOT NULL);
            """)


# Comando para crear tabla de usuario ¡¡¡¡¡¡¡Pendiente!!!!!!
cur.execute("""CREATE TABLE user_data(
            user_id SERIAL PRIMARY KEY,
            user_name VARCHAR (50) UNIQUE NOT NULL,
            password VARCHAR (24) NOT NULL);
            """)



# Cerrar el cursor y la bbdd
cur.close()
conn.close()