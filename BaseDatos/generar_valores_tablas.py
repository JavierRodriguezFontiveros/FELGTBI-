import psycopg2
from psycopg2.extras import DictCursor
import random
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


# Listas de valores para rellenar aleatoriamente las filas
ciudades = ["Salamanca", "Madrid", "Barcelona", "Cádiz", "Toledo", "Valencia", "Zaragoza", "A Coruña", "Sevilla"]
ambito_laboral = ["Hospitalario", "Centro de salud", "Asociación", "Centro comunitario"]
especialidad = ["Psicólogo", "Trabajador social", "Especialista en ETS", "Voluntario"]

# Generar 7 filas con datos aleatorios
for _ in range(7):
    ciudad = random.choice(ciudades)
    ambito = random.choice(ambito_laboral)
    especialidad_seleccionada = random.choice(especialidad)
    
    # Insertar los datos en la tabla
    cur.execute("""
        INSERT INTO sociosanitarios_data (ciudad, ambito_laboral, especialidad)
        VALUES (%s, %s, %s)
    """, (ciudad, ambito, especialidad_seleccionada))

# Confirmar los cambios
conn.commit()

conn.commit()
conn.close()
