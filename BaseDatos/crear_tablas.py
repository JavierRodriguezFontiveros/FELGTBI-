import psycopg2
from psycopg2.extras import DictCursor

import os
from dotenv import load_dotenv
import re

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
            admin_name VARCHAR (50) UNIQUE NOT NULL,
            password VARCHAR (24) NOT NULL);
            """)
# Grabar los cambios en la bbdd
conn.commit()
print("tabla admin creada")

# Comando para crear tabla de preguntas ------------------------ELIMINAAAAAAAAAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRRR
# cur.execute("""CREATE TABLE IF NOT EXISTS preguntas(
#             pregunta_id SERIAL PRIMARY KEY,
#             texto VARCHAR (200) NOT NULL);
#             """)
# Grabar los cambios en la bbdd
# conn.commit()
# print("tabla preguntas creada")

# Comando para crear tabla de preguntas
# cur.execute("""
#             CREATE TABLE IF NOT EXISTS preguntas_front (
#             id_categoria VARCHAR(10),  -- categoría en formato "1.1", "1.2", etc.
#             titulo_categoria VARCHAR(255),
#             texto_pregunta TEXT,
#             texto_opcion TEXT,
#             -- opcionalmente podemos generar un ID de opción único basado en la categoría
#             CONSTRAINT unique_categoria_opcion UNIQUE (id_categoria, texto_pregunta, texto_opcion));
#             """)
# # Grabar los cambios en la bbdd
# conn.commit()
# print("tabla preguntas creada")








# Crear tablas del arbol de decisión (alias: chatbot)
# cur.execute(
#   """
#   CREATE TABLE IF NOT EXISTS categorias_chatbot (
#     id_categoria SERIAL PRIMARY KEY,
#     titulo_categoria VARCHAR(500),
#     seccion VARCHAR(50)  -- Columna que puedes utilizar para indicar si pertenece a 'sociosanitario' o 'usuario'
# );
#   """
# )
# conn.commit()


# cur.execute(
#   """
#   CREATE TABLE IF NOT EXISTS preguntas_chatbot (
#     id_pregunta SERIAL PRIMARY KEY,
#     texto_pregunta TEXT NOT NULL UNIQUE
# );
#   """
# )
# conn.commit()


# cur.execute(
#   """
#   CREATE TABLE IF NOT EXISTS opciones_chatbot (
#     id_opcion INTEGER PRIMARY KEY AUTOINCREMENT,
#     texto_opcion TEXT NOT NULL
# );
#   """
# )
# conn.commit()
# print("tablas chatbot creadas")


# cur.execute(
#   """CREATE TABLE IF NOT EXISTS categoria_pregunta_chat_intermed (
#     id_categoria INT,
#     id_pregunta INT,
#     FOREIGN KEY (id_categoria) REFERENCES categorias_chatbot(id_categoria),
#     FOREIGN KEY (id_pregunta) REFERENCES preguntas_chatbot(id_pregunta)
# );"""
# )
# conn.commit()
# print("tablas categoria_pregunta_chat_intermed creada")

# cur.execute(
#   """CREATE TABLE IF NOT EXISTS preguntas_opciones_chatbot (
#     id_pregunta INT,
#     id_opcion INT,
#     PRIMARY KEY (id_pregunta, id_opcion),
#     FOREIGN KEY (id_pregunta) REFERENCES preguntas_chatbot(id_pregunta) ON DELETE CASCADE,
#     FOREIGN KEY (id_opcion) REFERENCES opciones_chatbot(id_opcion) ON DELETE CASCADE
# );
# """
# )
# conn.commit()
# print("tablas preguntas_opciones_chatbot creada")


# cur.execute(
#   """CREATE TABLE IF NOT EXISTS respuestas_modelo (
#     id_usuario VARCHAR(255) PRIMARY KEY NOT NULL,
#     respuesta_modelo TEXT
# );
# """
# )
# conn.commit()
# print('tabla respuestas_modelo creada')

# Comando para crear tabla de usuario ¡¡¡¡¡¡¡Pendiente!!!!!!
cur.execute("""CREATE TABLE IF NOT EXISTS no_sociosanit_formulario(
            edad INTEGER NOT NULL,
            pronombre_el BOOLEAN NOT NULL,
            pronombre_ella BOOLEAN NOT NULL,
            pronombre_elle BOOLEAN NOT NULL,
            identidad_genero VARCHAR(50) NOT NULL,
            orientacion_sexual VARCHAR(50) NOT NULL,
            vives_en_espana BOOLEAN NOT NULL,
            nacionalidad VARCHAR(50) NOT NULL,
            permiso_residencia BOOLEAN NOT NULL,
            persona_racializada BOOLEAN NOT NULL,
            persona_discapacitada BOOLEAN NOT NULL,
            persona_sin_hogar BOOLEAN NOT NULL,
            persona_migrante BOOLEAN NOT NULL,
            persona_intersexual BOOLEAN NOT NULL,
            nivel_estudios VARCHAR(50) NOT NULL,
            situacion_afectiva VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            id_usuario VARCHAR(255) PRIMARY KEY
            );
            """)
conn.commit()
print("tabla no sociosanitario creada")


cur.execute("""CREATE TABLE IF NOT EXISTS respuestas_chatbot_nosanitarios (
    id_usuario VARCHAR(255) PRIMARY KEY,
    pregunta1 TEXT,
    respuesta1 TEXT,
    response_array JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES no_sociosanit_formulario (id_usuario) ON DELETE CASCADE                
);""")

print('tabla respuestas_chatbot_nosanitarios creada')
conn.commit()



cur.execute("""CREATE TABLE IF NOT EXISTS respuestas_chatbot_tengo_vih (
    id_usuario VARCHAR(255) PRIMARY KEY,
    situacion VARCHAR(255),
    tiempo_diagnostico VARCHAR(255),
    tratamiento_tar VARCHAR(255),
    compartido_diagnostico VARCHAR(255), 
    acceso_recursos VARCHAR(255),
    acceso_personal_sanitario VARCHAR(255),
    recursos_informacion VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES respuestas_chatbot_nosanitarios (id_usuario) ON DELETE CASCADE                                             
);""")

print('tabla respuestas_chatbot_tengo_vih creada')
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS respuestas_chatbot_exposicion_vih (
    id_usuario VARCHAR(255) PRIMARY KEY,
    situacion VARCHAR(255),
    tiempo_exposicion VARCHAR(255),
    acceso_personal_sanitario VARCHAR(255),
    tipo_exposicion VARCHAR(255),
    entorno_chemsex VARCHAR(255),
    info_pep VARCHAR(255),    
    compartido_preocupacion VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES respuestas_chatbot_nosanitarios (id_usuario) ON DELETE CASCADE                                               
);""")

print('tabla respuestas_chatbot_exposicion_vih creada')
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS respuestas_chatbot_informacion_vih (
    id_usuario VARCHAR(255) PRIMARY KEY,
    situacion VARCHAR(255),
    recursos VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES respuestas_chatbot_nosanitarios (id_usuario) ON DELETE CASCADE                                            
);""")

print('tabla respuestas_chatbot_informacion_vih creada')
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS respuestas_chatbot_apoyo_persona_seropositiva (
    id_usuario VARCHAR(255) PRIMARY KEY,
    situacion VARCHAR(255),
    acceso_recursos VARCHAR(255),
    compartido_preocupacion VARCHAR(255),
    recursos_apoyo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES respuestas_chatbot_nosanitarios (id_usuario) ON DELETE CASCADE                                      
);""")

print('tabla respuestas_chatbot_exposicion_vih creada')
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS respuestas_chatbot_sanitarios (
    id_usuario VARCHAR(255) PRIMARY KEY,
    especialidad VARCHAR(255),
    recursos VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);""")

print('tabla respuestas_chatbot_sanitarios creada')
conn.commit()

# Comando para crear tabla de sociosanitarios ¡¡¡¡¡¡¡Pendiente!!!!!!
cur.execute("""CREATE TABLE IF NOT EXISTS sociosanitarios_formulario(
            ciudad VARCHAR (50) NOT NULL,
            ambito_laboral VARCHAR (50) NOT NULL,
            id_usuario VARCHAR(255) PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_usuario) REFERENCES  respuestas_chatbot_sanitarios(id_usuario) ON DELETE CASCADE
            );
            """)
conn.commit()
print("tabla sociosanitarios creada")



#Cerrar el cursor y la bbdd
cur.close()
conn.close() 
