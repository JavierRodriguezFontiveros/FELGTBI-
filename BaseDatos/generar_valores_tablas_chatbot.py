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


# Inserción en categorias_chatbot
categorias = [
    ('Personal Sanitario',),
    ('Trabajador Social ',),
    ('Psicologo',),
    ('Educador',),
    ('Voluntarios y Cuidadores',)
    ('Tengo vih'),
    ('Creo que me he expuesto al virus'),
    ('Quiero saber mas sobre el vih/sida'),
    ('Estoy apoyando a una persona seropositiva'),

]

cur.executemany("INSERT INTO categorias_chatbot (titulo_categoria) VALUES (%s);", categorias)

# Inserción en preguntas_chatbot
preguntas = [
    # preguntas Chatbot (sociosanitario)
    # PRIMARY id_pregunta, id_categoria, texto_pregunta
    (1, '¿Qué necesitas?'),
   
 
    # Preguntas Chatbot (Usuario no sociosanitario)
    (2, '¿Cuándo te diagnosticaron?'),
    (2, '¿Estás en tratamiento TAR?'),
    (2, '¿Tienes acceso a un médico'),
    (2, '¿Has compartido tu diagnostico con alguien?'),
    (2, '¿Quieres información sobre algun tema?'),
    (2, '¿Cuándo ocurrió la posible infección?'),
    (2, '¿Qué tipo de exposición fue?'),
    (2, '¿Ha sido en un entorno de "chem-sex"?'),
    (2, '¿Has compartido tu preocupación con alguien"?'),
    (2, '¿Sabes qué es la PEP?'),
    (2, '¿Necesitas recursos de referencia?'),
    (2, '¿Tienes acceso a recursos locales o grupos de apoyo?'),
    (2, '¿Qué apoyo necesitas?'),
    


]

cur.executemany("INSERT INTO preguntas_chatbot (id_categoria, texto_pregunta) VALUES (%s, %s);", preguntas)

# Inserción en opciones_chatbot
opciones = [
    # Opciones Iniciales
    (1, 'Personal sociosanitario'),
    (1, 'Usuario no sociosanitario'),
    
    # Preguntas Sociodemográficas (Personal Sociosanitario)
    (2, 'Listado de provincias'),
    (3, 'Centro de Salud'),
    (3, 'Hospital'),
    (3, 'Centro comunitario'),
    (3, 'Consulta privada'),
    (3, 'Asociación'),
    
    # Preguntas Sociodemográficas (Usuario no sociosanitario)
    (4, 'Número entre 14 y 100'),
    (5, 'Él'),
    (5, 'Ella'),
    (5, 'Elle'),
    (6, 'Hombre Cis'),
    (6, 'Hombre trans'),
    (6, 'Mujer Cis'),
    (6, 'Mujer trans'),
    (6, 'No binarie'),
    (6, 'Otro'),
    (7, 'Gay'),
    (7, 'Lesbiana'),
    (7, 'Bisexual'),
    (7, 'Pansexual'),
    (7, 'Asexual'),
    (7, 'Otro'),
    (8, 'Sí'),
    (8, 'No'),
    (9, 'Sí'),
    (9, 'No'),
    (10, 'Persona racializada'),
    (10, 'Discapacitade'),
    (10, 'Sin hogar'),
    (10, 'Migrante'),
    (10, 'Intersexual'),
    (11, 'Estudios universitarios'),
    (11, 'Bachillerato o grado superior'),
    (11, 'Educación básica'),
    (11, 'Sin estudios'),
    (12, 'Soltería'),
    (12, 'Pareja estable'),
    (12, 'Matrimonio'),
    (12, 'Otras'),
    
    # Preguntas Chatbot (Personal sociosanitario)
    (13, 'Personal sanitario'),
    (13, 'Trabajador social'),
    (13, 'Psicólogo'),
    (13, 'Educador'),
    (13, 'Voluntarios y cuidadores'),
    (14, 'Dependiendo de la especialidad seleccionada: Manejo clínico, Protocolo PEP, etc.'),
    
    # Preguntas Chatbot (Usuario no sociosanitario)
    (15, 'Tengo VIH'),
    (15, 'Creo que me he expuesto al virus'),
    (15, 'Quiero saber más sobre el VIH/SIDA'),
    (15, 'Estoy apoyando a una persona seropositiva'),
    (16, 'Ayuda emocional'),
    (16, 'Información sobre tratamientos'),
    (16, 'Recursos para cuidadores'),
    (16, 'Información sobre derechos')
]

cur.executemany("INSERT INTO opciones_chatbot (id_pregunta, texto_opcion) VALUES (%s, %s);", opciones)

# Confirmar transacciones y cerrar conexión
conn.commit()
cur.close()
conn.close()
