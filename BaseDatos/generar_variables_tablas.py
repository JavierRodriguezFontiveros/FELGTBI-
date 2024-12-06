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

# Agregamos nuevas variables a la tabla users
# cur.execute("""ALTER TABLE user_data 
#             ADD COLUMN pronombres VARCHAR(50),
#             ADD COLUMN genero VARCHAR(50),
#             ADD COLUMN orientacion VARCHAR(50),
#             ADD COLUMN pertenencia_colectivos VARCHAR(50),
#             ADD COLUMN vives_espana BOOLEAN,
#             ADD COLUMN pais VARCHAR(50),
#             ADD COLUMN permiso_residencia VARCHAR(50);
#             """)

# conn.commit()
# conn.close()
# print("Variables actualizadas")

# Modificar tipo variable permiso_residencia. SOLO USAR SI NO HAY DATOS

# cur.execute("""ALTER TABLE user_data 
# ALTER COLUMN permiso_residencia TYPE BOOLEAN 
# USING permiso_residencia::BOOLEAN; """)

# Agregamos nuevas variables a la tabla users y eliminamos pertenencia a colectivos
# cur.execute("""ALTER TABLE user_data 
#             DROP COLUMN pertenencia_colectivos,
#             DROP COLUMN permiso_residencia,
#             ADD COLUMN permiso_residencia VARCHAR(50),
#             ADD COLUMN persona_racializada BOOLEAN,
#             ADD COLUMN discapacitade BOOLEAN,
#             ADD COLUMN sin_hogar BOOLEAN,
#             ADD COLUMN migrante BOOLEAN;
#       """)
# conn.commit()

# Agregamos nuevas variables a la tabla users y eliminamos pertenencia a colectivos
cur.execute("""ALTER TABLE user_data 
            ADD COLUMN intersexual BOOLEAN;
      """)
conn.commit()

# Cerrar la conexión con la bbdd
conn.close()