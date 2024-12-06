import psycopg2
from psycopg2.extras import DictCursor
import random
import os
from dotenv import load_dotenv
import numpy as np

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

# Listas de valores que pueden tomar las columnas en la tabla de users_data para rellenar aleatoriamente las filas    
edad = np.arange(15,80)
pronombres = ["el", "ella", "elle"]
genero = ["hombre_cis", "hombre_trans", "mujer_cis", "mujer_trans", "no_binarie", "otro"]
orientacion = ["gay", "lesbiana", "bisexual", "heterosexual", "pansexual", "asexual", "otro"]
vives_espana = [True, False]
pais = ["España", "Marruecos", "Colombia", "Rumanía", "Venezuela", "Ecuador", "Argentina", "Reino Unido", "Perú", "Francia", "Alemania"]
permiso_residencia = ["Con permiso de residencia", "De vacaciones", "Permiso de residencia en trámite", "Otros"]
persona_racializada = [True, False]
discapacitade = [True, False]
sin_hogar = [True, False]
migrante = [True, False]
intersexual = [True, False]


# Generar 100 filas con datos aleatorios
for _ in range(100):
    edad_random = int(random.choice(edad))
    pronombres_random = random.choice(pronombres)
    genero_random = random.choice(genero)
    orientacion_random = random.choice(orientacion)
    vives_espana_random = random.choice(vives_espana)
    pais_random = random.choice(pais)
    permiso_residencia_random = random.choice(permiso_residencia)
    persona_racializada_random = random.choice(persona_racializada)
    discapacitade_random = random.choice(discapacitade)
    sin_hogar_random = random.choice(sin_hogar)
    migrante_random = random.choice(migrante)
    intersexual_random = random.choice(intersexual)
    

    # Insertar los datos en la tabla
    cur.execute("""
        INSERT INTO user_data (edad, pronombres, genero, orientacion, vives_espana, pais, permiso_residencia, persona_racializada, discapacitade, sin_hogar, migrante, intersexual)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (edad_random, pronombres_random, genero_random, orientacion_random, vives_espana_random, pais_random, permiso_residencia_random, persona_racializada_random, discapacitade_random, sin_hogar_random, migrante_random, intersexual_random))


# Confirmar los cambios
conn.commit()

# Listas de valores que pueden tomar las columnas en la tabla de sociosanitarios_data para rellenar aleatoriamente las filas
ciudades = ["Salamanca", "Madrid", "Barcelona", "Cádiz", "Toledo", "Valencia", "Zaragoza", "A Coruña", "Sevilla"]
ambito_laboral = ["Hospitalario", "Centro de salud", "Asociación", "Centro comunitario"]
especialidad = ["Psicólogo", "Trabajador social", "Especialista en ETS", "Voluntario"]

# Generar 100 filas con datos aleatorios
for _ in range(100):
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
