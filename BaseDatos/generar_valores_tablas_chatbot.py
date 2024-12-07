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
    ('Trabajador Social',),
    ('Psicologo',),
    ('Educador',),
    ('Voluntarios y Cuidadores',),
    ('Tengo vih',),
    ('Creo que me he expuesto al virus',),
    ('Quiero saber mas sobre el vih/sida',),
    ('Estoy apoyando a una persona seropositiva',),
]

#Inserción en preguntas_chatbot
cur.execute("SELECT id_categoria, titulo_categoria FROM categorias_chatbot;")
categorias = cur.fetchall()
categoria_dict = {categoria[1]: categoria[0] for categoria in categorias}
preguntas = [
    (categoria_dict['Personal Sanitario'], '¿Qué necesitas como Personal Sanitario?'),
    (categoria_dict['Trabajador Social'], '¿Qué necesitas como Trabajador Social?'),
    (categoria_dict['Psicologo'], '¿Qué necesitas como Psicologo?'),
    (categoria_dict['Educador'], '¿Qué necesitas como Educador?'),
    (categoria_dict['Voluntarios y Cuidadores'], '¿Qué necesitas como Voluntario/Cuidador?'),
    (categoria_dict['Tengo vih'], '¿Cuándo te diagnosticaron?'),
    (categoria_dict['Tengo vih'], '¿Estás en tratamiento TAR?'),
    (categoria_dict['Tengo vih'], '¿Tienes acceso a un médico?'),
    (categoria_dict['Tengo vih'], '¿Has compartido tu diagnostico con alguien?'),
    (categoria_dict['Tengo vih'], '¿Quieres información sobre algun tema?'),
    (categoria_dict['Creo que me he expuesto al virus'], '¿Cuándo ocurrió la posible infección?'),
    (categoria_dict['Creo que me he expuesto al virus'], '¿Qué tipo de exposición fue?'),
    (categoria_dict['Creo que me he expuesto al virus'], '¿Ha sido en un entorno de "chem-sex"?'),
    (categoria_dict['Creo que me he expuesto al virus'], '¿Tienes acceso a un médico?'),
    (categoria_dict['Creo que me he expuesto al virus'], '¿Has compartido tu preocupación con alguien?'),
    (categoria_dict['Creo que me he expuesto al virus'], '¿Sabes qué es la PEP?'),
    (categoria_dict['Quiero saber más sobre el vih/sida'], '¿Necesitas recursos de referencia?'),
    (categoria_dict['Estoy apoyando a una persona seropositiva'], '¿Tiene acceso a recursos locales o grupos de apoyo?'),
    (categoria_dict['Estoy apoyando a una persona seropositiva'], '¿Has compartido su preocupación sobre esta persona con alguien?'),
    (categoria_dict['Estoy apoyando a una persona seropositiva'], '¿Qué apoyo necesitas?'),
]

# Inserción en opciones_chatbot
cur.execute("SELECT id_pregunta, texto_pregunta FROM preguntas_chatbot;")
preguntas = cur.fetchall()
preguntas_dict = {pregunta[1]: pregunta[0] for pregunta in preguntas}
opciones = [
    (preguntas_dict['¿Qué necesitas como Personal Sanitario?'], 'Manejo clínico de pacientes con vih'),
    (preguntas_dict['¿Qué necesitas como Personal Sanitario?'], 'Protocolo PEP'),
    (preguntas_dict['¿Qué necesitas como Personal Sanitario?'], 'Tratamientos (PREP, TAR)'),
    (preguntas_dict['¿Qué necesitas como Personal Sanitario?'], 'Prevención de infecciones oportunistas'),
    (preguntas_dict['¿Qué necesitas como Personal Sanitario?'], 'Consejería para adherencia al tratamiento'),

    (preguntas_dict['¿Qué necesitas como Trabajador Social?'], 'Acceso a medicamentos o servicios'),
    (preguntas_dict['¿Qué necesitas como Trabajador Social?'], 'Recursos legales y derechos'),
    (preguntas_dict['¿Qué necesitas como Trabajador Social?'], 'Apoyo a personas en situación de vulnerabilidad'),
    (preguntas_dict['¿Qué necesitas como Trabajador Social?'], 'Conexión con grupos de apoyo comunitario'),
    (preguntas_dict['¿Qué necesitas como Trabajador Social?'], 'Información sobre redes de Servicios Sociales'),

    (preguntas_dict['¿Qué necesitas como Psicologo?'], 'Apoyo emocional para personas recién diagnosticadas'),
    (preguntas_dict['¿Qué necesitas como Psicologo?'], 'Intervenciones para adherencia al tratamiento'),
    (preguntas_dict['¿Qué necesitas como Psicologo?'], 'Manejo del estigma y problemas de salud menta'),
    (preguntas_dict['¿Qué necesitas como Psicologo?'], 'Recursos para pacientes con vih y trastornos psicológicos'),
    (preguntas_dict['¿Qué necesitas como Psicologo?'], 'Consejería en prevención y autocuidado'),

    (preguntas_dict['¿Qué necesitas como Educador?'], 'Material educativo sobre vih'),
    (preguntas_dict['¿Qué necesitas como Educador?'], 'Capacitación en prevención'),
    (preguntas_dict['¿Qué necesitas como Educador?'], 'Métodos para combatir el estigma'),
    (preguntas_dict['¿Qué necesitas como Educador?'], 'Recursos para sensibilización'),
    (preguntas_dict['¿Qué necesitas como Educador?'], 'Estadísticas y datos actualizados'),

    (preguntas_dict['¿Qué necesitas como Voluntario/Cuidador?'], 'Info básica sobre vih'),
    (preguntas_dict['¿Qué necesitas como Voluntario/Cuidador?'], 'Consejos para apoyar emocionalmente'),
    (preguntas_dict['¿Qué necesitas como Voluntario/Cuidador?'], 'Recursos legales y sociales para pacientes'),
    (preguntas_dict['¿Qué necesitas como Voluntario/Cuidador?'], 'Conexión con redes de apoyo'),
    (preguntas_dict['¿Qué necesitas como Voluntario/Cuidador?'], 'Métodos de autocuidado para cuidadores'),
    
    (preguntas_dict['¿Cuándo te diagnosticaron?'], 'Hace menos de 6 meses'),
    (preguntas_dict['¿Cuándo te diagnosticaron?'], 'Entre 6 meses y un año'),
    (preguntas_dict['¿Cuándo te diagnosticaron?'], 'Hace más de un año'),
    
    (preguntas_dict['¿Estás en tratamiento TAR?'], 'Sí'),
    (preguntas_dict['¿Estás en tratamiento TAR?'], 'No'),
    (preguntas_dict['¿Estás en tratamiento TAR?'], 'No estoy segure'),

    (preguntas_dict['¿Tienes acceso a un médico?'], 'Sí'),
    (preguntas_dict['¿Tienes acceso a un médico?'], 'No'),

    (preguntas_dict['¿Has compartido tu diagnostico con alguien?'], 'Un amigo'),
    (preguntas_dict['¿Has compartido tu diagnostico con alguien?'], 'Algún familiar'),
    (preguntas_dict['¿Has compartido tu diagnostico con alguien?'], 'Mi pareja en ese momento'),
    (preguntas_dict['¿Has compartido tu diagnostico con alguien?'], 'Compañero/a de trabajo'),
    (preguntas_dict['¿Has compartido tu diagnostico con alguien?'], 'Con mi jefe/a'),
    (preguntas_dict['¿Has compartido tu diagnostico con alguien?'], 'Personal de ONG'),
    (preguntas_dict['¿Has compartido tu diagnostico con alguien?'], 'Expareja'),
    (preguntas_dict['¿Has compartido tu diagnostico con alguien?'], 'Nadie'),

    (preguntas_dict['¿Quieres información sobre algun tema?'], 'Opciones de tratamiento'),
    (preguntas_dict['¿Quieres información sobre algun tema?'], 'Apoyo psicológico'),
    (preguntas_dict['¿Quieres información sobre algun tema?'], 'Derechos laborales y legales'),
    (preguntas_dict['¿Quieres información sobre algun tema?'], 'Grupos de apoyo'),
    (preguntas_dict['¿Quieres información sobre algun tema?'], 'Prevención de transmisión'),

    (preguntas_dict['¿Cuándo ocurrió la posible infección?'], 'Últimas 72h'),
    (preguntas_dict['¿Cuándo ocurrió la posible infección?'], 'Hace más de 72h'),

    (preguntas_dict['¿Qué tipo de exposición fue?'], 'Relación sexual'),
    (preguntas_dict['¿Qué tipo de exposición fue?'], 'Aguja compartida'),
    (preguntas_dict['¿Qué tipo de exposición fue?'], 'Contacto con fluidos corporales (sangre, fluido sexual..)'),
    (preguntas_dict['¿Qué tipo de exposición fue?'], 'No estoy segure'),

    (preguntas_dict['¿Ha sido en un entorno de "chem-sex"?'], 'Sí'),
    (preguntas_dict['¿Ha sido en un entorno de "chem-sex"?'], 'No'),

    (preguntas_dict['¿Tiene acceso a un médico?'], 'Sí'),
    (preguntas_dict['¿Tiene acceso a un médico?'], 'No'),

    (preguntas_dict['¿Has compartido tu preocupación con alguien?'], 'La persona que me preocupa'),
    (preguntas_dict['¿Has compartido tu preocupación con alguien?'], 'Un amigo'),
    (preguntas_dict['¿Has compartido tu preocupación con alguien?'], 'Algún familiar'),
    (preguntas_dict['¿Has compartido tu preocupación con alguien?'], 'Mi pareja en ese momento'),
    (preguntas_dict['¿Has compartido tu preocupación con alguien?'], 'Compañero/a de trabajo'),
    (preguntas_dict['¿Has compartido tu preocupación con alguien?'], 'Con mi jefe/a'),
    (preguntas_dict['¿Has compartido tu preocupación con alguien?'], 'Personal de ONG'),
    (preguntas_dict['¿Has compartido tu preocupación con alguien?'], 'Expareja'),
    (preguntas_dict['¿Has compartido tu preocupación con alguien?'], 'Nadie'),
 
    (preguntas_dict['¿Sabes qué es la PEP?'], 'Si, quiero más información'),
    (preguntas_dict['¿Sabes qué es la PEP?'], 'No ¿Qué es?'),

    (preguntas_dict['¿Necesitas recursos de referencia?'], '¿Qué es el vih/sida?'),
    (preguntas_dict['¿Necesitas recursos de referencia?'], 'Formas de transmisión'),
    (preguntas_dict['¿Necesitas recursos de referencia?'], 'Métodos de prevención'),
    (preguntas_dict['¿Necesitas recursos de referencia?'], 'Impacto del tratamiento'),
    (preguntas_dict['¿Necesitas recursos de referencia?'], 'Historia del vih'),

    (preguntas_dict['¿Tienes acceso a recursos locales o grupos de apoyo?'], 'Sí'),
    (preguntas_dict['¿Tienes acceso a recursos locales o grupos de apoyo?'], 'No'),

    (preguntas_dict['¿Has compartido su preocupación sobre esta persona con alguien?'], 'La persona que me preocupa'),
    (preguntas_dict['¿Has compartido su preocupación sobre esta persona con alguien?'], 'Un amigo'),
    (preguntas_dict['¿Has compartido su preocupación sobre esta persona con alguien?'], 'Algún familiar'),
    (preguntas_dict['¿Has compartido su preocupación sobre esta persona con alguien?'], 'Mi pareja en ese momento'),
    (preguntas_dict['¿Has compartido su preocupación sobre esta persona con alguien?'], 'Compañero/a de trabajo'),
    (preguntas_dict['¿Has compartido su preocupación sobre esta persona con alguien?'], 'Con mi jefe/a'),
    (preguntas_dict['¿Has compartido su preocupación sobre esta persona con alguien?'], 'Personal de ONG'),
    (preguntas_dict['¿Has compartido su preocupación sobre esta persona con alguien?'], 'Expareja'),
    (preguntas_dict['¿Has compartido su preocupación sobre esta persona con alguien?'], 'Nadie'),

    (preguntas_dict['¿Qué apoyo necesitas?'], 'Ayuda emocional'),
    (preguntas_dict['¿Qué apoyo necesitas?'], 'Información sobre tratamientos'),
    (preguntas_dict['¿Qué apoyo necesitas?'], 'Recursos para cuidadores'),
    (preguntas_dict['¿Qué apoyo necesitas?'], 'Información sobre derechos y apoyo social'),


]

try:
    cur.executemany("INSERT INTO categorias_chatbot (titulo_categoria) VALUES (%s);", categorias)
    cur.executemany("INSERT INTO preguntas_chatbot (id_categoria, texto_pregunta) VALUES (%s, %s);", preguntas)
    cur.executemany("INSERT INTO opciones_chatbot (id_pregunta, texto_opcion) VALUES (%s, %s);", opciones)
    conn.commit()
except Exception as e:
    conn.rollback()
    print(f"Error occurred: {e}")

# Confirmar transacciones y cerrar conexión
conn.commit()
cur.close()
conn.close()







""" 
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

cur.executemany("INSERT INTO opciones_chatbot (id_pregunta, texto_opcion) VALUES (%s, %s);", opciones) """