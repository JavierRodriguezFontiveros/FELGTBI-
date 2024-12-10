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
            admin_name VARCHAR (50) UNIQUE NOT NULL,
            password VARCHAR (24) NOT NULL);
            """)
# Grabar los cambios en la bbdd
conn.commit()
print("tabla admin creada")

# Comando para crear tabla de preguntas
cur.execute("""CREATE TABLE IF NOT EXISTS preguntas(
            pregunta_id SERIAL PRIMARY KEY,
            texto VARCHAR (200) NOT NULL);
            """)
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


cur.execute(
  """
  CREATE TABLE IF NOT EXISTS opciones_chatbot (
    id_opcion INTEGER PRIMARY KEY AUTOINCREMENT,
    texto_opcion TEXT NOT NULL
);
  """
)
conn.commit()
print("tablas chatbot creadas")


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


# Cerrar el cursor y la bbdd
cur.close()
conn.close() 
