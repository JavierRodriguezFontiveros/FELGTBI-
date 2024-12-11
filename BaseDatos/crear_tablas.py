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
conn.commit()
print("tabla preguntas creada")

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
cur.execute("""CREATE TABLE IF NOT EXISTS no_sociosanit_formulario(
            no_sociosanit_id SERIAL PRIMARY KEY,
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
            situacion_afectiva VARCHAR(50) NOT NULL);
            """)
conn.commit()
print("tabla no sociosanitario creada")




# Comando para crear tabla de sociosanitarios ¡¡¡¡¡¡¡Pendiente!!!!!!
cur.execute("""CREATE TABLE IF NOT EXISTS sociosanitarios_formulario(
            sociosanitario_id SERIAL PRIMARY KEY,
            ciudad VARCHAR (50) NOT NULL,
            ambito_laboral VARCHAR (50) NOT NULL
            );
            """)
conn.commit()
print("tabla sociosanitarios creada")


# Crear tablas del arbol de decisión (alias: chatbot)
cur.execute(
  """
  CREATE TABLE IF NOT EXISTS categorias_chatbot (
    id_categoria SERIAL PRIMARY KEY,
    titulo_categoria VARCHAR(500),
    seccion VARCHAR(50)  -- Columna que puedes utilizar para indicar si pertenece a 'sociosanitario' o 'usuario'
);
  """
)
conn.commit()


cur.execute(
  """
  CREATE TABLE IF NOT EXISTS preguntas_chatbot (
    id_pregunta SERIAL PRIMARY KEY,
    texto_pregunta TEXT NOT NULL UNIQUE
);
  """
)
conn.commit()


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


cur.execute(
  """CREATE TABLE IF NOT EXISTS categoria_pregunta_chat_intermed (
    id_categoria INT,
    id_pregunta INT,
    FOREIGN KEY (id_categoria) REFERENCES categorias_chatbot(id_categoria),
    FOREIGN KEY (id_pregunta) REFERENCES preguntas_chatbot(id_pregunta)
);"""
)
conn.commit()
print("tablas categoria_pregunta_chat_intermed creada")

cur.execute(
  """CREATE TABLE IF NOT EXISTS preguntas_opciones_chatbot (
    id_pregunta INT,
    id_opcion INT,
    PRIMARY KEY (id_pregunta, id_opcion),
    FOREIGN KEY (id_pregunta) REFERENCES preguntas_chatbot(id_pregunta) ON DELETE CASCADE,
    FOREIGN KEY (id_opcion) REFERENCES opciones_chatbot(id_opcion) ON DELETE CASCADE
);
"""
)
conn.commit()
print("tablas preguntas_opciones_chatbot creada")


cur.execute(
  """CREATE TABLE IF NOT EXISTS respuestas_modelo (
    id_usuario VARCHAR(255) PRIMARY KEY NOT NULL,
    respuesta_modelo TEXT
);
"""
)
conn.commit()
print('tabla respuestas_modelo creada')


cur.execute(
  """CREATE TABLE IF NOT EXISTS respuestas_personal_sanitario (
    id_usuario VARCHAR(255) PRIMARY KEY NOT NULL,
    especialidad VARCHAR(255),
    recursos VARCHAR(255)
);
"""
)
print('tabla respuestas_personal_sanitario creada')
conn.commit()

cur.execute(
  """CREATE TABLE IF NOT EXISTS respuestas_trabajador_social (
    id_usuario VARCHAR(255) PRIMARY KEY NOT NULL,
    especialidad VARCHAR(255),
    recursos VARCHAR(255)
);
"""
)
print('tabla respuestas_trabajador_social creada')
conn.commit()

cur.execute(
  """CREATE TABLE IF NOT EXISTS respuestas_psicólogo (
    id_usuario VARCHAR(255) PRIMARY KEY NOT NULL,
    especialidad VARCHAR(255),
    recursos VARCHAR(255)
);
"""
)
print('tabla respuestas_psicólogo creada')
conn.commit()

cur.execute(
  """CREATE TABLE IF NOT EXISTS respuestas_educador (
    id_usuario VARCHAR(255) PRIMARY KEY NOT NULL,
    especialidad VARCHAR(255),
    recursos VARCHAR(255)
);
"""
)
print('tabla respuestas_educador creada')
conn.commit()

cur.execute(
  """CREATE TABLE IF NOT EXISTS voluntario_y_cuidador (
    id_usuario VARCHAR(255) PRIMARY KEY NOT NULL,
    especialidad VARCHAR(255),
    recursos VARCHAR(255)
);
"""
)
print('tabla respuestas_voluntario_y_cuidador creada')
conn.commit()


cur.execute("""CREATE TABLE IF NOT EXISTS respuestas_chatbot_nosanitarios (
    id_usuario VARCHAR(255) PRIMARY KEY,
    pregunta1 TEXT,
    respuesta1 TEXT,
    response_array JSONB
);""")

print('tabla respuestas_chatbot_nosanitarios creada')
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS respuestas_chatbot_sanitarios (
    id_usuario VARCHAR(255) PRIMARY KEY,
    especialidad VARCHAR(255),
    recursos VARCHAR(255)
);""")

print('tabla respuestas_chatbot_sanitarios creada')
conn.commit()

# Obtener valores únicos de respuesta1 de no sanitarios
cur.execute("SELECT DISTINCT respuesta1 FROM respuestas_chatbot_nosanitarios")
unique_responses = cur.fetchall()  # Devuelve una lista de tuplas

for response in unique_responses:
    response_value = response[0]

    # Generar un nombre válido para la tabla
    table_name = re.sub(r'\W+', '_', response_value.lower())
    table_name = f"respuestas_chatbot_{table_name}"

    # Extraer valores únicos de response_array
    cur.execute(f"""
    SELECT DISTINCT jsonb_array_elements_text(response_array)
    FROM respuestas_chatbot_nosanitarios
    WHERE respuesta1 = %s
    """, (response_value,))
    unique_array_values = [row[0] for row in cur.fetchall()]  # Lista de valores únicos

    # Crear columnas dinámicamente
    dynamic_columns = ", ".join(
        [f"columna{i+1} TEXT" for i in range(len(unique_array_values))]
    )

    # Crear la tabla con columnas dinámicas

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id_usuario VARCHAR,
        pregunta1 TEXT,
        respuesta1 TEXT,
        {dynamic_columns}
    );
    """)
    conn.commit()

    # Poblar la tabla con los datos
    cur.execute(f"SELECT id_usuario, pregunta1, respuesta1, response_array FROM respuestas_chatbot_nosanitarios WHERE respuesta1 = %s",
                 (response_value,))
    rows = cur.fetchall()

    for row in rows:
        id_usuario, pregunta1, respuesta1, response_array = row
        
        # Convertir el array en una lista de valores
        response_values = [response_array[i] if i < len(response_array) else None for i in range(len(unique_array_values))]

        # Crear las columnas dinámicas para este registro
        column_names = ", ".join([f"columna{i+1}" for i in range(len(response_values))])
        placeholders = ", ".join(["%s"] * len(response_values))
        
        insert_query = f"""
        INSERT INTO {table_name} (id_usuario, pregunta1, respuesta1, {column_names})
        VALUES (%s, %s, %s, {placeholders})
        """
        cur.execute(insert_query, (id_usuario, pregunta1, respuesta1, *response_values))

# Confirmar cambios y cerrar conexión
conn.commit()

#Cerrar el cursor y la bbdd
cur.close()
conn.close() 
