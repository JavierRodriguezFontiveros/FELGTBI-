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

cur.execute("INSERT INTO user_data(edad) VALUES(20)")
print("Valor añadido") 
cur.execute("INSERT INTO user_data(edad) VALUES(35)")
print("Valor añadido")        
cur.execute("INSERT INTO user_data(edad) VALUES(42)")
print("Valor añadido")        
cur.execute("INSERT INTO user_data(edad) VALUES(61)") 
print("Valor añadido")       
cur.execute("INSERT INTO user_data(edad) VALUES(55)")
print("Valor añadido") 
cur.execute("INSERT INTO user_data(edad) VALUES(27)")
print("Valor añadido")          
cur.execute("INSERT INTO user_data(edad) VALUES(31)") 
print("Valor añadido")                     


conn.commit()
conn.close()
