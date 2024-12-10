# Bibliotecas:
from fastapi import FastAPI, Query #Api
import uvicorn #Despliegue en Local

import pandas as pd
import psycopg2
from psycopg2 import extras
from fastapi.responses import StreamingResponse
import io
import matplotlib.pyplot as plt

from utils import colectivos,connect_to_db,fetch_all_from_table, prompt_basico, modify_table_records,ambito_laboral

from io import BytesIO

from fastapi.responses import JSONResponse

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv
import os

import plotly.io as pio
from fastapi.responses import HTMLResponse

import json

from fastapi.middleware.cors import CORSMiddleware

# Configurar renderer
pio.renderers.default = "browser"

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


#CREAR API Y CONFIGURAR MODELO
app = FastAPI()
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=gemini_api_key)

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("Llamando al modelo con un prompt simple...")
    # response = model.generate_content("Prueba simple del modelo.")
    # print(f"Respuesta: {response.text}")
except Exception as e:
    print(f"Error al llamar al modelo: {e}")

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Configurar CORS


# Configurar orígenes permitidos
origins = [
    "http://localhost:5173",  # React u otras apps locales
    "https://felgtbiqplus.netlify.app",
    "https://chatbot-felgtbiq-front.onrender.com/"
    # Dominio de producción
]

# Añadir middleware de CORS
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,             # Orígenes permitidos
                   allow_credentials=True,            # Permitir credenciales como cookies o headers de autenticación
                   allow_methods=["*"],               # Métodos HTTP permitidos (GET, POST, PUT, DELETE, etc.)
                   allow_headers=["*"],               # Headers HTTP permitidos
)


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/")
async def home():
    return {"message": """
Hola buenas bienvenido a este proyecto de tripulaciones
                    """}



from utils import create_bar_chart_plotly_html,barras_apiladas_genero_orientacion_html,graficar_permiso_residencia_html,graficar_especialidad_html, grafico_pie,graficar_top_5_ciudades,check_admin_details
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
###FUNCIONA_EDITADA###
@app.get("/bar-chart/", response_class=HTMLResponse)
def generate_bar_chart():
    try:
        
        connection = connect_to_db()
        if connection is None:
            return {"error": "No se pudo conectar a la base de datos."}

        query = "SELECT * FROM no_sociosanit_formulario"

        df = pd.read_sql_query(query, connection)

        connection.close()

        html_content = create_bar_chart_plotly_html(df)

        return HTMLResponse(content=html_content, media_type="text/html")
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
###FUNCIONA_EDITADA###
@app.get("/pie-chart/", response_class=HTMLResponse)
def generar_grafico_pie(viven_espana: bool = True):
    try:
        # Conexión a la base de datos
        connection = connect_to_db()
        
        # Escribir la consulta SQL para obtener los datos
        query = "SELECT * FROM no_sociosanit_formulario"  # Cambia esta consulta según sea necesario

        # Usar pandas para ejecutar la consulta y convertirla en un DataFrame
        df = pd.read_sql_query(query, connection)
        
        # Cerrar la conexión después de obtener los datos
        connection.close()

        # Crear el gráfico de pastel
        fig = grafico_pie(df, viven_espana)

        # Exportar el gráfico como HTML
        html_content = fig.to_html(full_html=False)  # Genera solo el cuerpo del HTML

        # Devolver el HTML como respuesta
        return HTMLResponse(content=html_content, media_type="text/html")
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}
    


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
###FUNCIONA_EDITADA###
@app.get("/barras-apiladas/", response_class=HTMLResponse)
def generar_barras_apiladas():

    try:

        connection = connect_to_db()
        if connection is None:
            return {"error": "No se pudo conectar a la base de datos."}


        query = "SELECT * FROM no_sociosanit_formulario"  

        df = pd.read_sql_query(query, connection)

        connection.close()

        html_content = barras_apiladas_genero_orientacion_html(df)

        return HTMLResponse(content=html_content, media_type="text/html")
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}
    


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/grafico-permiso-residencia/", response_class=HTMLResponse)
def generar_grafico_permiso_residencia():
    """
    Endpoint para generar y mostrar un gráfico de permisos de residencia en HTML.
    """
    try:
        # Conectar a la base de datos
        connection = connect_to_db()
        if connection is None:
            return {"error": "No se pudo conectar a la base de datos."}

        # Escribir la consulta SQL para obtener los datos
        query = "SELECT * FROM no_sociosanit_formulario"  # Cambia esta consulta según sea necesario

        # Usar pandas para ejecutar la consulta y convertirla en un DataFrame
        df = pd.read_sql_query(query, connection)

        # Cerrar la conexión después de obtener los datos
        connection.close()

        # Generar el gráfico de permisos de residencia como HTML
        html_content = graficar_permiso_residencia_html(df)

        # Devolver el HTML como respuesta
        return HTMLResponse(content=html_content, media_type="text/html")
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}
    


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/colectivos/", response_class=HTMLResponse)
def generar_grafico_combinaciones():
    try:
        # Conectar a la base de datos
        connection = connect_to_db()

        # Escribir la consulta SQL para obtener los datos
        query = "SELECT * FROM no_sociosanit_formulario"  # Cambia esta consulta según sea necesario
        df = pd.read_sql_query(query, connection)

        # Cerrar la conexión después de obtener los datos
        connection.close()

        # Generar el gráfico interactivo
        fig = colectivos(df)

        # Obtener el gráfico como HTML interactivo
        html_content = fig.to_html(full_html=False)

        # Devolver el gráfico interactivo como respuesta
        return HTMLResponse(content=html_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocurrió un error al procesar el gráfico: {e}")
    


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
###FUNCIONA_EDITADA###
@app.get("/top-5-ciudades/", response_class=HTMLResponse)
def generate_bar_chart():
    try:
        # Conectar a la base de datos
        connection = connect_to_db()
        if connection is None:
            return {"error": "No se pudo conectar a la base de datos."}

        # Consulta SQL para obtener los datos
        query = "SELECT * FROM no_sociosanit_formulario"  # Asegúrate de usar el nombre correcto de la tabla

        # Cargar los datos en un DataFrame
        df = pd.read_sql_query(query, connection)

        # Cerrar la conexión
        connection.close()

        # Generar el gráfico de barras
        fig = graficar_top_5_ciudades(df)

        # Convertir el gráfico a HTML
        html_content = fig.to_html(full_html=False)

        # Devolver el HTML del gráfico
        return HTMLResponse(content=html_content, media_type="text/html")
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}
    
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/grafico-ambito-laboral/", response_class=HTMLResponse)
def generate_ambito_laboral_chart():
    """
    Endpoint para generar y mostrar un gráfico de ámbito laboral en HTML.
    """
    try:
        # Conectar a la base de datos
        connection = connect_to_db()
        if connection is None:
            return {"error": "No se pudo conectar a la base de datos."}

        # Consulta SQL para obtener los datos
        query = "SELECT * FROM sociosanitarios_formulario"  # Cambia el nombre de la tabla si es necesario

        # Cargar los datos en un DataFrame
        df = pd.read_sql_query(query, connection)

        # Cerrar la conexión
        connection.close()

        # Generar el gráfico de ámbito laboral
        fig = ambito_laboral(df)

        # Convertir el gráfico a HTML
        html_content = fig.to_html(full_html=False)

        # Devolver el HTML del gráfico
        return HTMLResponse(content=html_content, media_type="text/html")
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from enum import Enum


class GenderIdentity(str, Enum):
    hombre_cis = "Hombre cis"
    hombre_trans = "Hombre trans"
    mujer_cis = "Mujer cis"
    mujer_trans = "Mujer trans"
    no_binario = "No binarie"
    otro = "Otro"

class SexualOrientation(str, Enum):
    gay = "Gay"
    lesbiana = "Lesbiana"
    bisexual = "Bisexual"
    pansexual = "Pansexual"
    asexual = "Asexual"
    otro = "Otro"


class EducationLevel(str, Enum):
    primarios = "Primarios"
    secundarios = "Secundarios"
    tecnicos = "Técnicos"
    universitarios = "Universitarios"
    postgrado = "Postgrado"
    otro = "Otro"

class AffectiveSituation(str, Enum):
    soltero = "Soltere"
    en_pareja = "En pareja"
    casado = "Casade"
    divorciado = "Divorciade"
    viudo = "Viude"
    otro = "Otro"

class Nacionalidad(str,Enum):
    afganistan = "Afganistán"
    albania = "Albania"
    alemania = "Alemania"
    andorra = "Andorra"
    angola = "Angola"
    antigua_y_barbuda = "Antigua y Barbuda"
    argentina = "Argentina"
    armenia = "Armenia"
    australia = "Australia"
    austria = "Austria"
    azerbaiyan = "Azerbaiyán"
    bahamas = "Bahamas"
    banglades = "Bangladés"
    barbados = "Barbados"
    bielorrusia = "Bielorrusia"
    belgica = "Bélgica"
    belice = "Belice"
    benin = "Benín"
    bolivia = "Bolivia"
    bosnia_y_herzegovina = "Bosnia y Herzegovina"
    botsuana = "Botsuana"
    brasil = "Brasil"
    brunei = "Brunéi"
    bulgaria = "Bulgaria"
    burundi = "Burundi"
    butan = "Bután"
    cabo_verde = "Cabo Verde"
    camboya = "Camboya"
    camerun = "Camerún"
    canada = "Canadá"
    chad = "Chad"
    chile = "Chile"
    china = "China"
    chipre = "Chipre"
    colombia = "Colombia"
    comoras = "Comoras"
    republica_del_congo = "República del Congo"
    costa_rica = "Costa Rica"
    croacia = "Croacia"
    cuba = "Cuba"
    dinamarca = "Dinamarca"
    republica_dominicana = "República Dominicana"
    ecuador = "Ecuador"
    egipto = "Egipto"
    emiratos_arabes_unidos = "Emiratos Árabes Unidos"
    guinea_ecuatorial = "Guinea Ecuatorial"
    eslovaquia = "Eslovaquia"
    eslovenia = "Eslovenia"
    españa = "España"
    estados_unidos = "Estados Unidos"
    estonia = "Estonia"
    etiopia = "Etiopía"
    fiyi = "Fiyi"
    filipinas = "Filipinas"
    finlandia = "Finlandia"
    francia = "Francia"
    gabon = "Gabón"
    gambia = "Gambia"
    georgia = "Georgia"
    ghana = "Ghana"
    granada = "Granada"
    guatemala = "Guatemala"
    guinea = "Guinea"
    guyana = "Guyana"
    haiti = "Haití"
    honduras = "Honduras"
    hong_kong = "Hong Kong"
    hungria = "Hungría"
    islandia = "Islandia"
    india = "India"
    indonesia = "Indonesia"
    irak = "Irak"
    iran = "Irán"
    israel = "Israel"
    italia = "Italia"
    jamaica = "Jamaica"
    japon = "Japón"
    jordania = "Jordania"
    kenia = "Kenia"
    kirguistan = "Kirguistán"
    kosovo = "Kosovo"
    kuwait = "Kuwait"
    laos = "Laos"
    letonia = "Letonia"
    lesoto = "Lesoto"
    liberia = "Liberia"
    libia = "Libia"
    liechtenstein = "Liechtenstein"
    lituania = "Lituania"
    luxemburgo = "Luxemburgo"
    macedonia_del_norte = "Macedonia del Norte"
    madagascar = "Madagascar"
    malaui = "Malaui"
    malasia = "Malasia"
    maldivas = "Maldivas"
    mali = "Malí"
    costa_de_marfil = "Costa de Marfil"
    mauricio = "Mauricio"
    mauritania = "Mauritania"
    mexico = "México"
    myanmar = "Myanmar"
    moldavia = "Moldavia"
    monaco = "Mónaco"
    mongolia = "Mongolia"
    mozambique = "Mozambique"
    namibia = "Namibia"
    nauru = "Nauru"
    nepal = "Nepal"
    nicaragua = "Nicaragua"
    nigeria = "Nigeria"
    noruega = "Noruega"
    nueva_zelanda = "Nueva Zelanda"
    niger = "Níger"
    palestina = "Palestina"
    panama = "Panamá"
    papua_nueva_guinea = "Papúa Nueva Guinea"
    paraguay = "Paraguay"
    peru = "Perú"
    polonia = "Polonia"
    portugal = "Portugal"
    catar = "Catar"
    reino_unido = "Reino Unido"
    republica_checa = "República Checa"
    ruanda = "Ruanda"
    rumania = "Rumanía"
    rusia = "Rusia"
    el_salvador = "El Salvador"
    samoa = "Samoa"
    san_cristobal_y_nieves = "San Cristóbal y Nieves"
    san_marino = "San Marino"
    santo_tome_y_principe = "Santo Tomé y Príncipe"
    senegal = "Senegal"
    serbia = "Serbia"
    seychelles = "Seychelles"
    sierra_leona = "Sierra Leona"
    singapur = "Singapur"
    siria = "Siria"
    somalia = "Somalia"
    sri_lanka = "Sri Lanka"
    sudafrica = "Sudáfrica"
    sudan = "Sudán"
    surinam = "Surinam"
    suecia = "Suecia"
    suiza = "Suiza"
    sudan_del_sur = "Sudán del Sur"
    esuatini = "Esuatini"
    tailandia = "Tailandia"
    tanzania = "Tanzania"
    togo = "Togo"
    tonga = "Tonga"
    trinidad_y_tobago = "Trinidad y Tobago"
    tunez = "Túnez"
    turquia = "Turquía"
    turkmenistan = "Turkmenistán"
    tuvalu = "Tuvalu"
    ucrania = "Ucrania"
    uganda = "Uganda"
    uruguay = "Uruguay"
    uzbekistan = "Uzbekistán"
    vanuatu = "Vanuatu"
    venezuela = "Venezuela"
    vietnam = "Vietnam"
    yemen = "Yemen"
    yugoslavia = "Yugoslavia"
    zambia = "Zambia"
    zimbabue = "Zimbabue"

class Province(str, Enum):
    alava = "Álava"
    albacete = "Albacete"
    alicante = "Alicante"
    almeria = "Almería"
    avila = "Ávila"
    badajoz = "Badajoz"
    barcelona = "Barcelona"
    burgos = "Burgos"
    caceres = "Cáceres"
    cadiz = "Cádiz"
    cantabria = "Cantabria"
    castellon = "Castellón"
    ceuta = "Ceuta"
    cordoba = "Córdoba"
    cuenca = "Cuenca"
    girona = "Girona"
    granada = "Granada"
    guadalajara = "Guadalajara"
    huelva = "Huelva"
    huesca = "Huesca"
    jaen = "Jaén"
    la_rioja = "La Rioja"
    las_palmas = "Las Palmas"
    leon = "León"
    lugo = "Lugo"
    madrid = "Madrid"
    malaga = "Málaga"
    melilla = "Melilla"
    murcia = "Murcia"
    navarra = "Navarra"
    ourense = "Ourense"
    palencia = "Palencia"
    pontevedra = "Pontevedra"
    salamanca = "Salamanca"
    segovia = "Segovia"
    sevilla = "Sevilla"
    soria = "Soria"
    tarragona = "Tarragona"
    teruel = "Teruel"
    toledo = "Toledo"
    valencia = "Valencia"
    valladolid = "Valladolid"
    vizcaya = "Vizcaya"
    zamora = "Zamora"
    zaragoza = "Zaragoza"
    fuera_espana = "Fuera de España"

#Clase Completa
class UserData(BaseModel):
    id_usuario: str
    edad: int

    pronombre_el: bool  
    pronombre_ella: bool  
    pronombre_elle: bool  

    identidad_genero: GenderIdentity
    orientacion_sexual: SexualOrientation
    vives_en_espana: bool
    nacionalidad: Nacionalidad  
    permiso_residencia: bool


    persona_racializada: bool  
    persona_discapacitada: bool  
    persona_sin_hogar: bool  
    persona_migrante: bool  
    persona_intersexual: bool
    

    nivel_estudios: EducationLevel  
    situacion_afectiva: AffectiveSituation 
    provincia: Province

@app.post("/submit-data")
async def submit_data(user_data: UserData):
    connection = connect_to_db()
    if connection is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
    
    cursor = connection.cursor()

    # Aquí ajustamos la consulta y los datos
    query = """
            INSERT INTO no_sociosanit_formulario (edad, pronombre_el, pronombre_ella, pronombre_elle, identidad_genero,
                                                orientacion_sexual, vives_en_espana, nacionalidad, permiso_residencia,
                                                persona_racializada, persona_discapacitada, persona_sin_hogar,
                                                persona_migrante, persona_intersexual, nivel_estudios, situacion_afectiva,
                                                provincia, id_usuario)
            VALUES (%(edad)s, %(pronombre_el)s, %(pronombre_ella)s, %(pronombre_elle)s, %(identidad_genero)s,
                    %(orientacion_sexual)s, %(vives_en_espana)s, %(nacionalidad)s, %(permiso_residencia)s,
                    %(persona_racializada)s, %(persona_discapacitada)s, %(persona_sin_hogar)s, %(persona_migrante)s,
                    %(persona_intersexual)s, %(nivel_estudios)s, %(situacion_afectiva)s, %(provincia)s, %(id_usuario)s)
    """
    
    data = {
            "edad": user_data.edad,
            "id_usuario": user_data.id_usuario,
            "pronombre_el": user_data.pronombre_el,
            "pronombre_ella": user_data.pronombre_ella,
            "pronombre_elle": user_data.pronombre_elle,
            "identidad_genero": user_data.identidad_genero,
            "orientacion_sexual": user_data.orientacion_sexual,
            "vives_en_espana": user_data.vives_en_espana,
            "nacionalidad": user_data.nacionalidad,
            "permiso_residencia": user_data.permiso_residencia,
            "persona_racializada": user_data.persona_racializada,
            "persona_discapacitada": user_data.persona_discapacitada,
            "persona_sin_hogar": user_data.persona_sin_hogar,
            "persona_migrante": user_data.persona_migrante,
            "persona_intersexual": user_data.persona_intersexual,
            "nivel_estudios": user_data.nivel_estudios,
            "situacion_afectiva": user_data.situacion_afectiva,
            "provincia": user_data.provincia
            }

    try:
        cursor.execute(query, data)
        connection.commit()
        return {"message": "Datos enviados y almacenados correctamente"}
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        connection.rollback()
        raise HTTPException(status_code=500, detail="Error al guardar los datos")
    finally:
        cursor.close()
        connection.close()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class WorkEnvironment(str, Enum):
    centro_salud = "Centro de salud"
    hospital = "Hospital"
    centro_comunitario = "Centro comunitario"
    consulta_privada = "Consulta privada"
    asociacion = "Asociación"
    otro = "Otro"

class SociosanitaryData(BaseModel):
    id_usuario: str
    provincia: Province
    ambito_laboral: WorkEnvironment 


@app.post("/submit-data-2")
async def submit_data(sociosanitary_data: SociosanitaryData):
    connection = connect_to_db()
    if connection is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
    
    cursor = connection.cursor()

    # Aquí ajustamos la consulta y los datos
    query = """
            INSERT INTO sociosanitarios_formulario (provincia, 
                                                    ambito_laboral, id_usuario)
            VALUES (%(provincia)s, %(ambito_laboral)s, %(id_usuario)s)
    """
    
    data = {
            "provincia": sociosanitary_data.provincia,
            "ambito_laboral": sociosanitary_data.ambito_laboral,
            "id_usuario": sociosanitary_data.id_usuario
            }

    try:
        cursor.execute(query, data)
        connection.commit()
        return {"message": "Datos enviados y almacenados correctamente"}
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        connection.rollback()
        raise HTTPException(status_code=500, detail="Error al guardar los datos")
    finally:
        cursor.close()
        connection.close()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class UserData(BaseModel):
    data: Dict[str, Any]

import concurrent.futures

def generar_respuesta(prompt):
    try:
        def call_model():
            model = genai.GenerativeModel("gemini-1.5-flash")
            return model.generate_content(prompt + prompt_basico)

        # Usar un executor para manejar el tiempo límite
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(call_model)
            response = future.result(timeout=30)  # Tiempo límite de 30 segundos

        # Verificar si la respuesta es válida
        if not response or not hasattr(response, 'text'):
            raise ValueError("Respuesta vacía o no válida del modelo.")
        return response.text
    except concurrent.futures.TimeoutError:
        print("El modelo tomó demasiado tiempo en responder.")
        return "Error: El modelo tardó demasiado en responder."
    except Exception as e:
        print(f"Error en generar_respuesta: {e}")
        return f"Error al generar respuesta para historia: {str(e)}"
    
def generar_respuesta_final(prompt_chat, memory):
    try:
        def call_model():
            model = genai.GenerativeModel("gemini-1.5-flash")
            return model.generate_content("Teniendo en cuenta lo que acabamos de hablar (" + str(memory) + "), resuélveme esta consulta:" + prompt_chat)

        # Usar un executor para manejar el tiempo límite
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(call_model)
            response = future.result(timeout=30)  # Tiempo límite de 30 segundos

        # Verificar si la respuesta es válida
        if not response or not hasattr(response, 'text'):
            raise ValueError("Respuesta vacía o no válida del modelo.")
        return response.text
    except concurrent.futures.TimeoutError:
        print("El modelo tomó demasiado tiempo en responder.")
        return "Error: El modelo tardó demasiado en responder."
    except Exception as e:
        print(f"Error en generar_respuesta: {e}")
        return f"Error al generar respuesta para historia: {str(e)}"


@app.post("/personalizar_prompt_usuario_no_ss")
async def personalizar_prompt_usuario_no_ss(user_data: UserData):
    print(f"API Key en uso: {gemini_api_key}")

    try:
        # Determinar el tipo de sección y construir el prompt dinámicamente
        for key, seccion in user_data.data.items():
            titulo = seccion.get("titulo", " ")
            preguntas = seccion.get("preguntas", {})

# SI NO ES SOCIOSANITARIO

            if key.startswith("1"):
    #EXTRAER ID_USUARIO
                id_usuario = None

                id_usuario = seccion.get("id_usuario")
                # id_usuario = str(id_usuario)
                print(f"ID Usuario recibido: {id_usuario}")   
                if not id_usuario.isalnum():
                    return {"error": "ID de usuario no válido."}     
                
                connection = connect_to_db()

                if connection is None:
                    return {"error": "No se pudo conectar a la base de datos."}

                cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

                try:
                    # Escribir la consulta SQL para obtener los datos
                    query = """
                        SELECT provincia, pronombre_elle, pronombre_el, pronombre_ella
                        FROM no_sociosanit_formulario
                        WHERE id_usuario = %s
                    """
                    cursor.execute(query, (id_usuario,))

                    # Obtener el resultado de la consulta
                    resultados = cursor.fetchone()

                    if not resultados:
                        return {"error": "No se encontraron datos para el ID de usuario proporcionado."}
                
                    provincia = resultados["provincia"]
                    pronombres = []

                    if resultados["pronombre_el"]:
                        pronombres.append("Él")
                    if resultados["pronombre_ella"]:
                        pronombres.append("Ella")
                    if resultados["pronombre_elle"]:
                        pronombres.append("Elle/Pronombre neutro")

                    pronombres = ", ".join(pronombres)

                except Exception as e:
                    # Cerrar la conexión en caso de error
                    if connection:
                        cursor.close()
                        connection.close()
                    return {"error": f"Error al procesar la solicitud: {str(e)}"}
                cursor.close()
                connection.close()
## TRAS EXTRAER DATOS, CONFECCIONAR PROMPT
                if key.startswith("1.1"):
                    tiempo_diagnostico = preguntas.get("¿Cuándo te diagnosticaron?", [""])[0]
                    en_tratamiento = preguntas.get("¿Estás en tratamiento TAR?", [""])[0]
                    acceso_medico = preguntas.get("¿Tienes acceso a un médico?", [""])[0]
                    informacion_necesaria = preguntas.get("¿Quieres información sobre algún tema?", ["Ninguna"])[0]

                    # Crear el prompt para la sección 1.1
                    prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Tengo VIH diagnosticado desde " + tiempo_diagnostico + ". \n"
                            "¿Qué si estoy en tratamiento?" + en_tratamiento + ". \n"
                            ". Y además " + acceso_medico + ". \n"
                            "tengo acceso médico. La información que solicito es:"+ informacion_necesaria + "."
                    )

                elif key.startswith("1.2"):
                    tipo_exposicion = preguntas.get("¿Qué tipo de exposición fue?", [" "])[0]
                    tiempo_exposicion = preguntas.get("¿Cuándo ocurrió la posible infección?", [" "])[0]
                    acceso_medico = preguntas.get("¿Tienes acceso a un médico?", [" "])[0]
                    chem_sex = preguntas.get("¿Ha sido en un entorno de 'chem-sex'?", [" "])[0]
                    preocupacion = preguntas.get("¿Has compartido tu preocupación con alguien?", [" "])[0]
                    conocimiento_pep = preguntas.get("¿Sabes qué es la PEP?", [" "])[0]

                    # Crear el prompt para la sección 1.2
                    prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Creo que me he expuesto al virus en " + tiempo_exposicion + ". \n"
                            "El tipo de exposición ha sido:" + tipo_exposicion + ". \n"
                            + chem_sex + "ha sido en entorno de chem-sex. \n"
                            "He compartido mi preocupación con"+ preocupacion + "Y quiero más información sobre la PEP."
                    )

                elif key.startswith("1.3"):
                    tema_informacion = preguntas.get("¿Sobre qué tema quieres información?", [" "])[0]

                    # Crear el prompt para la sección 1.3
                    prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Quiero información sobre:" + tema_informacion)

                elif key.startswith("1.4"):
                    acceso_grupos = preguntas.get("¿Tienes acceso a recursos locales o grupos de apoyo?", [" "])[0]
                    preocupacion4 = preguntas.get("¿Has compartido tu preocupación con alguien?", [" "])[0]
                    apoyo_necesario = preguntas.get("¿Qué apoyo necesitas?", [" "])[0]

                    # Crear el prompt para la sección 1.4
                    prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                            "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                            "Estoy acompañando a una persona seropositiva." + acceso_grupos + "tengo acceso a recursos locales o grupos de apoyo. /n"
                            "He compartido mi preocupación con" + preocupacion4 + ". /n"
                            "Me gustaría orientación para conseguir" + apoyo_necesario)

                # Generar la respuesta del modelo
                respuesta_chatbot = generar_respuesta(prompt)

                # Devolver la respuesta del chatbot
                return {"respuesta_chatbot": respuesta_chatbot}
        else:
            prompt = "Título: "

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post("/personalizar_prompt_usuario_ss")
async def personalizar_prompt_usuario_ss(user_data: UserData):
    print(f"API Key en uso: {gemini_api_key}")
    try:
        for key, seccion in user_data.data.items():
            titulo = seccion.get("titulo", " ")
            preguntas = seccion.get("preguntas", {})
            id_usuario = seccion.get("id_usuario")

            if not id_usuario or not id_usuario.isalnum():
                return {"error": "ID de usuario no válido."}

            connection = connect_to_db()
            if connection is None:
                return {"error": "No se pudo conectar a la base de datos."}

            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            try:
                query = """
                    SELECT ambito_laboral, provincia
                    FROM sociosanitarios_formulario
                    WHERE id_usuario = %s
                """
                cursor.execute(query, (id_usuario,))
                resultados = cursor.fetchone()

                if not resultados:
                    return {"error": "No se encontraron datos para el ID de usuario proporcionado."}

                provincia = resultados["provincia"]
                ambito_laboral = resultados["ambito_laboral"]
            except Exception as e:
                cursor.close()
                connection.close()
                return {"error": f"Error al procesar la solicitud: {str(e)}"}

            cursor.close()
            connection.close()

            eleccion = preguntas.get("¿Qué necesitas?", [" "])[0]
            prompt = (
                f"Mi pronombre es el neutro (elle). "
                f"Vivo en {provincia}. Dame respuestas orientadas a ese lugar.\n"
                f"Soy personal sanitario y trabajo en este ámbito laboral: {ambito_laboral}.\n"
                f"Estoy trabajando actualmente con vih (úsalo siempre en minúscula). Necesito información profesional sobre {eleccion}."
            )

            respuesta_chatbot = generar_respuesta(prompt)
            return {"respuesta_chatbot": respuesta_chatbot}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### CHATBOT FINAL DE CONVERSACIÓN, ENTRADA DE TEXTO

memory = ""

@app.get("/chatbot")
async def chatbot(prompt_chat: str = Query(None), memory = str):  ## IMPORTAR QUERY EN FASTAPI

    try:
        respuesta = generar_respuesta_final(prompt_chat, memory)
        return {"respuesta_chatbot": respuesta}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/preguntas_user/")
async def preguntas_user(): 
    try:
        # Conexión a la base de datos
        connection = connect_to_db()
        
        # Escribir la consulta SQL para obtener los datos
        query_usuarios = """
                    SELECT 
                        c.id_categoria,
                        p.id_pregunta,
                        o.id_opcion,
                        c.titulo_categoria,
                        p.texto_pregunta,
                        o.texto_opcion
                    FROM 
                        categorias_chatbot c
                    JOIN 
                        categoria_pregunta_chat_intermed cp ON c.id_categoria = cp.id_categoria
                    JOIN 
                        preguntas_chatbot p ON cp.id_pregunta = p.id_pregunta
                    JOIN 
                        preguntas_opciones_chatbot po ON p.id_pregunta = po.id_pregunta
                    JOIN 
                        opciones_chatbot o ON po.id_opcion = o.id_opcion
                    WHERE 
                        c.seccion = 'usuario'
                    ORDER BY 
                        c.id_categoria, p.id_pregunta, o.id_opcion;
                    """

        # Usar pandas para ejecutar la consulta y convertirla en un DataFrame
        df = pd.read_sql_query(query_usuarios, connection)
        
        grouped_questions = (
            df.groupby(['id_categoria', 'titulo_categoria', 'id_pregunta', 'texto_pregunta'])
            .apply(lambda x: x[['id_opcion', 'texto_opcion']].to_dict(orient='records'))
            .reset_index()
            .rename(columns={0: 'opciones'})
        )
        
        # Convertir las preguntas a una lista estructurada por categorías
        result = (
            grouped_questions.groupby(['id_categoria', 'titulo_categoria'])
            .apply(lambda x: x[['id_pregunta', 'texto_pregunta', 'opciones']].to_dict(orient='records'))
            .reset_index()
            .rename(columns={0: 'preguntas'})
            .to_dict(orient='records')
        )
        
        # # json_data = df.to_dict(orient="records")
        # json_data = json.dumps(result, indent=3, ensure_ascii=False)
        
        connection.close()

        return result
    
    except Exception as e:
        return {"error": f"Ha ocurrido algún problema obteniendo las preguntas: {e}"}
    
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/preguntas_sociosanitarios/")
async def preguntas_user(): 
    try:
        # Conexión a la base de datos
        connection = connect_to_db()
        
        # Escribir la consulta SQL para obtener los datos
        query_sociosanitarios = """
                            SELECT 
                                c.id_categoria,
                                p.id_pregunta,
                                o.id_opcion,
                                c.titulo_categoria,
                                p.texto_pregunta,
                                o.texto_opcion
                            FROM 
                                categorias_chatbot c
                            JOIN 
                                categoria_pregunta_chat_intermed cp ON c.id_categoria = cp.id_categoria
                            JOIN 
                                preguntas_chatbot p ON cp.id_pregunta = p.id_pregunta
                            JOIN 
                                preguntas_opciones_chatbot po ON p.id_pregunta = po.id_pregunta
                            JOIN 
                                opciones_chatbot o ON po.id_opcion = o.id_opcion
                            WHERE 
                                c.seccion = 'sociosanitario'
                            ORDER BY 
                                c.id_categoria, p.id_pregunta, o.id_opcion;
                        """

        # Usar pandas para ejecutar la consulta y convertirla en un DataFrame
        df = pd.read_sql_query(query_sociosanitarios, connection)
        
        grouped_questions = (
            df.groupby(['id_categoria', 'titulo_categoria', 'id_pregunta', 'texto_pregunta'])
            .apply(lambda x: x[['id_opcion', 'texto_opcion']].to_dict(orient='records'))
            .reset_index()
            .rename(columns={0: 'opciones'})
            )
        
        # Convertir las preguntas a una lista estructurada por categorías
        result = (
            grouped_questions.groupby(['id_categoria', 'titulo_categoria'])
            .apply(lambda x: x[['id_pregunta', 'texto_pregunta', 'opciones']].to_dict(orient='records'))
            .reset_index()
            .rename(columns={0: 'preguntas'})
            .to_dict(orient='records')
        )
        
        # json_data = df.to_dict(orient="records")
        # json_data = json.dumps(result, indent=3, ensure_ascii=False)
        
        # print(json_data)
        
        connection.close()

        return result
    
    except Exception as e:
        return {"error": f"Ha ocurrido algún problema obteniendo las preguntas: {e}"}


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



@app.get("/get-table/{table_name}")
def get_table_data(table_name: str):
    try:
        data = fetch_all_from_table(table_name)
        return {"table_name": table_name, "data": data}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

@app.put("/modify-records/")
async def modify_records_endpoint(
    table_name: str, 
    column: str, 
    new_value: str, 
    id: int
):
    try:
        modify_table_records(table_name, column, new_value, id)
        return {"message": "Record successfully modified."}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


class AdminLogin(BaseModel):
    email: str
    password: str

@app.post("/admin/login")
async def admin_login(admin: AdminLogin):
    # Call the check_admin_details function with the provided email and password
    is_valid = check_admin_details(admin.email, admin.password)
    
    if is_valid:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    # Punto de entrada principal
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

# {
#   "data": {
#     "1.1": {
#       "id_usuario" : "1234abcd",
#       "titulo": "Tengo VIH",
#       "preguntas": {
#         "¿Cuándo te diagnosticaron?": ["Hace menos de 6 meses"],
#         "¿Estás en tratamiento TAR?": ["Sí"],
#         "¿Tienes acceso a un médico?": ["Sí"],
#         "¿Quieres información sobre algún tema?": ["Apoyo psicológico"]
#       }
#     }
#   }
# }

# {
#   "data": {
#     "2.1": {
#       "id_usuario" : "789abc",
#       "titulo": "Personal sanitario",
#       "preguntas": {
#         "¿Qué necesitas?" : ["Manejo clínico de pacientes con VIH"]
#       }
#     }
#   }
# }
