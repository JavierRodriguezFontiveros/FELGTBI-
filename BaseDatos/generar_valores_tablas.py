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
pronombre_el = [True, False]
pronombre_ella = [True, False]
pronombre_elle = [True, False]
genero = ["hombre_cis", "hombre_trans", "mujer_cis", "mujer_trans", "no_binarie", "otro"]
orientacion = ["gay", "lesbiana", "bisexual", "heterosexual", "pansexual", "asexual", "otro"]
vives_espana = [True, False]
nacionalidad = ["Afganistán", "Albania", "Alemania", "Andorra", "Angola", "Antigua y Barbuda", "Argentina", "Armenia", "Australia", 
        "Austria", "Azerbaiyán", "Bahamas", "Bangladés", "Barbados", "Bielorrusia", "Bélgica", "Belice", "Benín", "Bolivia", "Bosnia y Herzegovina", 
        "Botsuana", "Brasil", "Brunéi", "Bulgaria", "Burundi", "Bután", "Cabo Verde", "Camboya", "Camerún", "Canadá", "Chad", "Chile", "China", "Chipre", 
        "Colombia", "Comoras", "República del Congo", "Costa Rica", "Croacia", "Cuba", "Dinamarca", "República Dominicana", "Ecuador", "Egipto", "Emiratos Árabes Unidos", 
        "Guinea Ecuatorial", "Eslovaquia", "Eslovenia", "España", "Estados Unidos", "Estonia", "Etiopía", "Fiyi", "Filipinas", "Finlandia", "Francia", "Gabón", "Gambia", "Georgia", 
        "Ghana", "Granada", "Guatemala", "Guinea", "Guinea Ecuatorial", "Guyana", "Haití", "Honduras", "Hong Kong", "Hungría", "Islandia", "India", "Indonesia", "Irak", "Irán", "Israel", 
        "Italia", "Jamaica", "Japón", "Jordania", "Kenia", "Kirguistán", "Kosovo", "Kuwait", "Laos", "Letonia", "Lesoto", "Liberia", "Libia", "Liechtenstein", "Lituania", "Luxemburgo", 
        "Macedonia del Norte", "Madagascar", "Malaui", "Malasia", "Maldivas", "Malí", "Costa de Marfil", "Mauricio", "Mauritania", "México", "Myanmar", "Moldavia", "Mónaco", "Mongolia", 
        "Mozambique", "Namibia", "Nauru", "Nepal", "Nicaragua", "Nigeria", "Noruega", "Nueva Zelanda", "Níger", "Palestina", "Panamá", "Papúa Nueva Guinea", "Paraguay", "Perú", "Polonia", 
        "Portugal", "Catar", "Reino Unido", "República Checa", "República Dominicana", "Ruanda", "Rumanía", "Rusia", "El Salvador", "Samoa", "San Cristóbal y Nieves", "San Marino", 
        "Santo Tomé y Príncipe", "Senegal", "Serbia", "Seychelles", "Sierra Leona", "Singapur", "Siria", "Somalia", "Sri Lanka", "Sudáfrica", "Sudán", "Surinam", "Suecia", "Suiza", 
        "Sudán del Sur", "Esuatini", "Tailandia", "Tanzania", "Togo", "Tonga", "Trinidad y Tobago", "Túnez", "Turquía", "Turkmenistán", "Tuvalu", "Ucrania", "Uganda", "Uruguay", 
        "Uzbekistán", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Yugoslavia", "Zambia", "Zimbabue"]
permiso_residencia = ["Con permiso de residencia", "De vacaciones", "Permiso de residencia en trámite", "Otros"]
persona_racializada = [True, False]
discapacitade = [True, False]
sin_hogar = [True, False]
migrante = [True, False]
intersexual = [True, False]
provincia = ["Álava", "Albacete", "Alicante", "Almería", "Ávila", "Badajoz", "Barcelona", "Burgos", "Cáceres",
              "Cádiz", "Cantabria", "Castellón", "Ceuta", "Córdoba", "Cuenca", "Girona", "Granada", "Guadalajara", "Huelva", 
              "Huesca", "Jaén", "La Rioja", "Las Palmas", "León", "Lugo", "Madrid", "Málaga", "Melilla", "Murcia", "Navarra", "Ourense", 
              "Palencia", "Pontevedra", "Salamanca", "Segovia", "Sevilla", "Soria", "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid", 
              "Vizcaya", "Zamora", "Zaragoza", "Fuera de España"]

# Generar 100 filas con datos aleatorios
for _ in range(100):
    edad_random = int(random.choice(edad))
    pronombre_el_random = random.choice(pronombre_el)
    pronombre_ella_random = random.choice(pronombre_ella)
    pronombre_elle_random = random.choice(pronombre_elle)
    genero_random = random.choice(genero)
    orientacion_random = random.choice(orientacion)
    vives_espana_random = random.choice(vives_espana)
    nacionalidad_random = random.choice(nacionalidad)
    permiso_residencia_random = random.choice(permiso_residencia)
    persona_racializada_random = random.choice(persona_racializada)
    discapacitade_random = random.choice(discapacitade)
    sin_hogar_random = random.choice(sin_hogar)
    migrante_random = random.choice(migrante)
    intersexual_random = random.choice(intersexual)
    provincia_random = random.choice(provincia)

    # Insertar los datos en la tabla
    cur.execute("""
        INSERT INTO no_sociosanit_formulario (edad, pronombre_el, pronombre_ella, pronombre_elle, identidad_genero,
                                                orientacion_sexual, vives_en_espana, nacionalidad, permiso_residencia,
                                                persona_racializada, persona_discapacitada, persona_sin_hogar,
                                                persona_migrante, persona_intersexual, nivel_estudios, situacion_afectiva,
                                                provincia)
           VALUES (%(edad)s, %(pronombre_el)s, %(pronombre_ella)s, %(pronombre_elle)s, %(identidad_genero)s,
                   %(orientacion_sexual)s, %(vives_en_espana)s, %(nacionalidad)s, %(permiso_residencia)s,
                   %(persona_racializada)s, %(persona_discapacitada)s, %(persona_sin_hogar)s, %(persona_migrante)s,
                   %(persona_intersexual)s, %(nivel_estudios)s, %(situacion_afectiva)s, %(provincia)s)
    """, 
    (edad_random, pronombre_el_random, pronombre_ella_random, pronombre_elle_random, genero_random, orientacion_random, vives_espana_random, nacionalidad_random, permiso_residencia_random, persona_racializada_random, discapacitade_random, sin_hogar_random, migrante_random, intersexual_random))


# Confirmar los cambios
conn.commit()

# Listas de valores que pueden tomar las columnas en la tabla de sociosanitarios_data para rellenar aleatoriamente las filas
ambito_laboral = ["Hospitalario", "Centro de salud", "Asociación", "Centro comunitario"]
#especialidad = ["Trabajador social", "Especialista en ETS", "Voluntarios y cuidadores", "Personal sanitario", "Educador"]

# Generar 100 filas con datos aleatorios
for _ in range(100):
    provincia_random = random.choice(provincia)
    ambito = random.choice(ambito_laboral)
    #especialidad_seleccionada = random.choice(especialidad)
    
    # Insertar los datos en la tabla
    cur.execute("""
        INSERT INTO sociosanitarios_data (provincia, ambito_laboral, especialidad)
        VALUES (%s, %s, %s)
    """, (provincia_random, ambito, especialidad_seleccionada))

# Confirmar los cambios
conn.commit()

# cur.execute("""
#     INSERT INTO preguntas_front (id_categoria, titulo_categoria, texto_pregunta, texto_opcion) VALUES
#     ('1.1.1', 'Tengo VIH', '¿Cuándo te diagnosticaron?', 'Hace menos de 6 meses'),
#     ('1.1.2', 'Tengo VIH', '¿Cuándo te diagnosticaron?', 'Entre 6 meses y un año'),
#     ('1.1.3', 'Tengo VIH', '¿Cuándo te diagnosticaron?', 'Hace más de un año'),
#     ('1.1.4', 'Tengo VIH', '¿Estás en tratamiento TAR?', 'Sí'),
#     ('1.1.5', 'Tengo VIH', '¿Estás en tratamiento TAR?', 'No'),
#     ('1.1.6', 'Tengo VIH', '¿Estás en tratamiento TAR?', 'No estoy seguro'),
#     ('1.1.7', 'Tengo VIH', '¿Tienes acceso a un médico?', 'Sí'),
#     ('1.1.8', 'Tengo VIH', '¿Tienes acceso a un médico?', 'No'),
#     ('1.2.1', 'Creo que me he expuesto al virus', '¿Cuándo ocurrió la posible infección?', 'Últimas 72h'),
#     ('1.2.2', 'Creo que me he expuesto al virus', '¿Cuándo ocurrió la posible infección?', 'Hace más de 72h'),
#     ('1.2.3', 'Creo que me he expuesto al virus', '¿Qué tipo de exposición fue?', 'Relación sexual'),
#     ('1.2.4', 'Creo que me he expuesto al virus', '¿Qué tipo de exposición fue?', 'Aguja compartida'),
#     ('1.2.5', 'Creo que me he expuesto al virus', '¿Qué tipo de exposición fue?', 'Contacto con fluidos corporales'),
#     ('1.2.6', 'Creo que me he expuesto al virus', '¿Qué tipo de exposición fue?', 'No estoy seguro'),
#     ('1.2.7', 'Creo que me he expuesto al virus', '¿Ha sido en un entorno de “chem-sex”?', 'Sí'),
#     ('1.2.8', 'Creo que me he expuesto al virus', '¿Ha sido en un entorno de “chem-sex”?', 'No'),
#     ('1.2.9', 'Creo que me he expuesto al virus', '¿Tienes acceso a un médico?', 'Sí'),
#     ('1.2.10', 'Creo que me he expuesto al virus', '¿Tienes acceso a un médico?', 'No'),
#     ('1.2.11', 'Creo que me he expuesto al virus', '¿Sabes que es la PEP?', 'Sí, quiero más información'),
#     ('1.2.12', 'Creo que me he expuesto al virus', '¿Sabes que es la PEP?', 'No ¿Qué es?')
# """)

# conn.commit()
conn.close()
