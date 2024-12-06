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

# cur.execute("INSERT INTO user_data(edad) VALUES(20)")
# print("Valor añadido") 
# cur.execute("INSERT INTO user_data(edad) VALUES(35)")
# print("Valor añadido")        
# cur.execute("INSERT INTO user_data(edad) VALUES(42)")
# print("Valor añadido")        
# cur.execute("INSERT INTO user_data(edad) VALUES(61)") 
# print("Valor añadido")       
# cur.execute("INSERT INTO user_data(edad) VALUES(55)")
# print("Valor añadido") 
# cur.execute("INSERT INTO user_data(edad) VALUES(27)")
# print("Valor añadido")          
# cur.execute("INSERT INTO user_data(edad) VALUES(31)") 
# print("Valor añadido")


cur.execute("""
    INSERT INTO preguntas_front (id_categoria, titulo_categoria, texto_pregunta, texto_opcion) VALUES
    ('1.1.1', 'Tengo VIH', '¿Cuándo te diagnosticaron?', 'Hace menos de 6 meses'),
    ('1.1.2', 'Tengo VIH', '¿Cuándo te diagnosticaron?', 'Entre 6 meses y un año'),
    ('1.1.3', 'Tengo VIH', '¿Cuándo te diagnosticaron?', 'Hace más de un año'),
    ('1.1.4', 'Tengo VIH', '¿Estás en tratamiento TAR?', 'Sí'),
    ('1.1.5', 'Tengo VIH', '¿Estás en tratamiento TAR?', 'No'),
    ('1.1.6', 'Tengo VIH', '¿Estás en tratamiento TAR?', 'No estoy seguro'),
    ('1.1.7', 'Tengo VIH', '¿Tienes acceso a un médico?', 'Sí'),
    ('1.1.8', 'Tengo VIH', '¿Tienes acceso a un médico?', 'No'),
    ('1.2.1', 'Creo que me he expuesto al virus', '¿Cuándo ocurrió la posible infección?', 'Últimas 72h'),
    ('1.2.2', 'Creo que me he expuesto al virus', '¿Cuándo ocurrió la posible infección?', 'Hace más de 72h'),
    ('1.2.3', 'Creo que me he expuesto al virus', '¿Qué tipo de exposición fue?', 'Relación sexual'),
    ('1.2.4', 'Creo que me he expuesto al virus', '¿Qué tipo de exposición fue?', 'Aguja compartida'),
    ('1.2.5', 'Creo que me he expuesto al virus', '¿Qué tipo de exposición fue?', 'Contacto con fluidos corporales'),
    ('1.2.6', 'Creo que me he expuesto al virus', '¿Qué tipo de exposición fue?', 'No estoy seguro'),
    ('1.2.7', 'Creo que me he expuesto al virus', '¿Ha sido en un entorno de “chem-sex”?', 'Sí'),
    ('1.2.8', 'Creo que me he expuesto al virus', '¿Ha sido en un entorno de “chem-sex”?', 'No'),
    ('1.2.9', 'Creo que me he expuesto al virus', '¿Tienes acceso a un médico?', 'Sí'),
    ('1.2.10', 'Creo que me he expuesto al virus', '¿Tienes acceso a un médico?', 'No'),
    ('1.2.11', 'Creo que me he expuesto al virus', '¿Sabes que es la PEP?', 'Sí, quiero más información'),
    ('1.2.12', 'Creo que me he expuesto al virus', '¿Sabes que es la PEP?', 'No ¿Qué es?')
""")

conn.commit()
conn.close()
