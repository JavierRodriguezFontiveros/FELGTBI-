# Bibliotecas:
from fastapi import FastAPI, Query #Api
import uvicorn #Despliegue en Local

import pandas as pd
import psycopg2
from psycopg2 import extras
from fastapi.responses import StreamingResponse
import io
import matplotlib.pyplot as plt

from utils import colectivos,connect_to_db,fetch_all_from_table, prompt_basico, modify_table_records, graficar_permiso_residencia_html,ambito_laboral

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

from langchain_community.tools import GooglePlacesTool

#Warnings
import warnings
warnings.filterwarnings("ignore")

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
    "https://chatbot-felgtbiq-front.onrender.com"
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



from utils import create_bar_chart_plotly_html,barras_apiladas_genero_orientacion_html,graficar_permiso_residencia_html, grafico_pie,graficar_top_5_ciudades,check_admin_details
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
        with connect_to_db() as connection:
            query = "SELECT * FROM no_sociosanit_formulario"
            df = pd.read_sql_query(query, connection)

        if df.empty:
            return {"error": "La consulta no devolvió resultados."}

        html_content = barras_apiladas_genero_orientacion_html(df)

        return HTMLResponse(content=html_content, media_type="text/html")
    except ValueError as ve:
        return {"error": f"Error de validación: {ve}"}
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}
    


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
###FUNCIONA_EDITADA###
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
###FUNCIONA_EDITADA###
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
            return HTMLResponse(content="Error: No se pudo conectar a la base de datos.", media_type="text/html")

        # Consulta SQL para obtener los datos
        query = "SELECT * FROM no_sociosanit_formulario"  # Asegúrate de usar el nombre correcto de la tabla

        # Cargar los datos en un DataFrame
        df = pd.read_sql_query(query, connection)

        # Cerrar la conexión
        connection.close()

        # Verificar el contenido del DataFrame
        if df.empty:
            return HTMLResponse(content="Error: No se encontraron datos en la tabla.", media_type="text/html")

        # Generar el gráfico de barras
        fig = graficar_top_5_ciudades(df)

        # Convertir el gráfico a HTML
        html_content = fig.to_html(full_html=False)

        # Devolver el HTML del gráfico
        return HTMLResponse(content=html_content, media_type="text/html")
    except Exception as e:
        error_message = f"Error al procesar el gráfico: {e}"
        return HTMLResponse(content=error_message, media_type="text/html")
    
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
        html_content = ambito_laboral(df)

        # Devolver el HTML del gráfico
        return HTMLResponse(content=html_content, media_type="text/html")
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
###GRÁFICOS-CHATBOT###




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
    heterosexual = "Heterosexual"
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


from utils import generar_respuesta, generar_respuesta_final


import re

@app.post("/personalizar_prompt_usuario_no_ss")
async def personalizar_prompt_usuario_no_ss(data: dict):
    print(f"API Key en uso: {gemini_api_key}")
    try:
        # Validar que el JSON tiene la estructura esperada
        if "data" not in data or not isinstance(data["data"], list):
            return {"error": "Formato de datos no válido. Se requiere un JSON con la clave 'data' y un array de valores."}
        # Extraer el array del JSON
        values = data["data"]
        if len(values) < 2:
            return {"error": "El array debe contener al menos dos elementos."}
        # Extraer el ID del usuario y la situación
        id_usuario = values[0]
        situacion = values[2]  # Según el formato, la situación está en el tercer elemento
        if not id_usuario or not isinstance(id_usuario, str) or not id_usuario.isalnum():
            return {"error": "ID de usuario no válido."}
        connection = connect_to_db()
        if connection is None:
            return {"error": "No se pudo conectar a la base de datos."}
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            # Obtener los datos del usuario desde la base de datos
            query = """
                SELECT provincia, pronombre_elle, pronombre_el, pronombre_ella
                FROM no_sociosanit_formulario
                WHERE id_usuario = %s
            """
            cursor.execute(query, (id_usuario,))
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
            cursor.close()
            connection.close()
            return {"error": f"Error al procesar la solicitud: {str(e)}"}
##################################EDITADO############
        #Configuracion de la API google Places:
        load_dotenv(dotenv_path="../credenciales.env")
        google_places = os.getenv("GPLACES_API_KEY")
        os.environ["GPLACES_API_KEY"] = google_places
        # Crear instancia de GooglePlacesTool
        places = GooglePlacesTool()
        # Realizar la búsqueda
        try:
            prompt_maps = f"Centros vih " + provincia
            respuesta_google_maps = places.run(prompt_maps)
            pattern = re.compile(r"(\d+)\.\s*(.*?)\nAddress:\s*(.*?)\nGoogle place ID:\s*(.*?)\nPhone:\s*(.*?)\nWebsite:\s*(.*?)\n", re.DOTALL)
            matches = pattern.findall(respuesta_google_maps)

            matches = list({match[0]: match for match in matches}.values())

            matches = matches[:3]  # Muestra solo los primeros 3 resultados

            locations_str = ""
            for match in matches:
                location_info = (
                    f"ID: {int(match[0])}\n"
                    f"Name: {match[1].strip()}\n"
                    f"Address: {match[2].strip()}\n"
                    f"Phone: {match[4].strip() if match[4].strip() != 'Unknown' else 'N/A'}\n"
                    f"Website: {match[5].strip() if match[5].strip() != 'Unknown' else 'N/A'}\n"
                    f"{'-' * 40}\n"  # Separador entre cada ubicación
                )
                locations_str += location_info

            # Imprimir el resultado en consola
            print(locations_str)
            print(provincia)

        except Exception as e:
            print(f"Hubo un error al realizar la búsqueda: {e}")
#######################################################
        # Construcción del prompt basado en la situación
        prompt = ""
        if situacion == "Tengo vih":
            tiempo_diagnostico = values[4]
            en_tratamiento = values[6]
            acceso_medico = values[8]
            informacion_necesaria = values[10]
            prompt = (
                f"Mis pronombres son: {pronombres}. \n"
                f"Vivo en {provincia}. Dame respuestas orientadas a ese lugar.\n"
                f"Tengo vih diagnosticado desde {tiempo_diagnostico}. \n"
                f"¿Estoy en tratamiento TAR? {en_tratamiento}. \n"
                f"Tengo acceso a un médico: {acceso_medico}. \n"
                f"Necesito información sobre: {informacion_necesaria}."
            )
        elif situacion == "Creo que me he expuesto al virus":
            tiempo_exposicion = values[4]
            acceso_medico = values[6]
            tipo_exposicion = values[8]
            chem_sex = values[10]
            conocimiento_pep = values[12]
            preocupacion = values[14]
            prompt = (
                f"Mis pronombres son: {pronombres}. \n"
                f"Vivo en {provincia}. Dame respuestas orientadas a ese lugar.\n"
                f"Creo que me he expuesto al virus en {tiempo_exposicion}. \n"
                f"El tipo de exposición fue: {tipo_exposicion}. \n"
                f"{chem_sex}, ha sido en un entorno de chem-sex. \n"
                f"Tengo acceso médico: {acceso_medico}. \n"
                f"Quiero más información sobre la PEP. \n"
                f"Compartí mi preocupación con: {preocupacion}."
            )
        elif situacion == "Quiero saber más sobre el vih/sida":
            tema_informacion = values[4]
            prompt = (
                f"Mis pronombres son: {pronombres}. \n"
                f"Vivo en {provincia}. Dame respuestas orientadas a ese lugar.\n"
                f"Quiero información sobre: {tema_informacion}."
            )
        elif situacion == "Estoy apoyando a una persona seropositiva":
            acceso_grupos = values[4]
            preocupacion = values[6]
            apoyo_necesario = values[8]
            prompt = (
                f"Mis pronombres son: {pronombres}. \n"
                f"Vivo en {provincia}. Dame respuestas orientadas a ese lugar.\n"
                f"Estoy apoyando a una persona seropositiva. {acceso_grupos}.\n"
                f"Compartí mi preocupación con: {preocupacion}. \n"
                f"Me gustaría orientación para conseguir: {apoyo_necesario}."
            )
        else:
            return {"error": f"Situación no soportada: '{situacion}'"}
        # Generar respuesta del chatbot
        respuesta_chatbot = generar_respuesta(prompt)
        raw_data = data["data"]
        # Query adaptada para guardar los registros del chatbot de no sanitarios
        query = """INSERT INTO respuestas_chatbot_nosanitarios
        (id_usuario, pregunta1, respuesta1, response_array)
        VALUES (%s, %s, %s, %s)"""
        # Asignar los datos a los placeholders
        datos_no_ss = (
            raw_data[0], raw_data[1], raw_data[2], json.dumps(raw_data[3:])
        )
        cursor.execute(query, datos_no_ss)
        connection.commit()

    
        # Insertar las respuestas del chatbot en la tabla correspondiente
        id_usuario = raw_data[0]
        respuesta1 = raw_data[2]
        response_array = raw_data[3:]

        # Mapear los valores del array 'response_array' en las columnas correspondientes

        if "Tengo vih" in respuesta1:
            # Para la situación "Tengo vih"
            situacion = respuesta1
            tiempo_diagnostico = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Cuándo te diagnosticaron?"), None)
            tratamiento_tar = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Estás en tratamiento TAR?"), None)
            compartido_diagnostico = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Has compartido tu diagnóstico con alguien?"), None)
            acceso_recursos = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Tienes acceso a recursos locales o grupos de apoyo?"), None)
            acceso_personal_sanitario = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Tienes acceso a personal sanitario?"), None)
            recursos_informacion = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Quieres más información sobre algún tema?"), None)

            # Insertar en la tabla respuestas_chatbot_tengo_vih
            cursor.execute("""
                INSERT INTO respuestas_chatbot_tengo_vih (
                    id_usuario, situacion, tiempo_diagnostico, tratamiento_tar, compartido_diagnostico, 
                    acceso_recursos, acceso_personal_sanitario, recursos_informacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_usuario, situacion, tiempo_diagnostico, tratamiento_tar, compartido_diagnostico, acceso_recursos, acceso_personal_sanitario, recursos_informacion))
            connection.commit()

        elif "Creo que me he expuesto al virus" in respuesta1:
            # Para la situación de "Creo que me he expuesto al virus"
            situacion = respuesta1
            tiempo_exposicion = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Cuándo ocurrió la posible infección?"), None)
            acceso_personal_sanitario = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Tienes acceso a personal sanitario?"), None)
            tipo_exposicion = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Qué tipo de exposición fue?"), None)
            entorno_chemsex = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Ha sido en un entorno de 'chem-sex'?"), None)
            info_pep = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Sabes qué es la PEP?"), None)
            compartido_preocupacion = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Has compartido tu preocupación con alguien?"), None)

            # Insertar en la tabla respuestas_chatbot_exposicion_vih
            cursor.execute("""
                INSERT INTO respuestas_chatbot_exposicion_vih (
                    id_usuario, situacion, tiempo_exposicion, acceso_personal_sanitario, tipo_exposicion, 
                    entorno_chemsex, info_pep, compartido_preocupacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_usuario, situacion, tiempo_exposicion, acceso_personal_sanitario, tipo_exposicion, entorno_chemsex, info_pep, compartido_preocupacion))
            connection.commit()

        elif "Quiero saber más sobre el vih/sida" in respuesta1:
            # Para la situación de "Quiero saber más sobre el vih/sida"
            situacion = respuesta1
            recursos = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Necesitas recursos de referencia?"), None)

            # Insertar en la tabla respuestas_chatbot_informacion_vih
            cursor.execute("""
                INSERT INTO respuestas_chatbot_informacion_vih (
                    id_usuario, situacion, recursos
                ) VALUES (%s, %s, %s)
            """, (id_usuario, situacion, recursos))
            connection.commit()

        elif "Estoy apoyando a una persona seropositiva" in respuesta1:
            # Para la situación de "Estoy apoyando a una persona seropositiva"
            situacion = respuesta1
            acceso_recursos = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Tiene acceso a recursos locales o grupos de apoyo?"), None)
            compartido_preocupacion = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Has compartido tu preocupación sobre esta persona con alguien?"), None)
            recursos_apoyo = next((response_array[i+1] for i in range(len(response_array)) if response_array[i] == "¿Qué apoyo necesitas?"), None)

            # Insertar en la tabla respuestas_chatbot_apoyo_persona_seropositiva
            cursor.execute("""
                INSERT INTO respuestas_chatbot_apoyo_persona_seropositiva (
                    id_usuario, situacion, acceso_recursos, compartido_preocupacion, recursos_apoyo
                ) VALUES (%s, %s, %s, %s, %s)
            """, (id_usuario, situacion, acceso_recursos, compartido_preocupacion, recursos_apoyo))
            connection.commit()


        # Insertar respuesta en la base de datos
        query = '''
            INSERT INTO respuestas_modelo (id_usuario, respuesta_modelo)
            VALUES (%s, %s)
            ON CONFLICT (id_usuario) DO UPDATE
            SET respuesta_modelo = EXCLUDED.respuesta_modelo;
        '''
        valores = (id_usuario, respuesta_chatbot)
########LOQUE HE AÑADIDO########
        respuesta_final = respuesta_chatbot + locations_str
################################
        cursor.execute(query, valores)
        connection.commit()
        cursor.close()
        connection.close()
        print("Datos insertados correctamente.")
        return {"respuesta_chatbot": respuesta_final}###################
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            print("Error cerrando la conexión.")

    

@app.post("/personalizar_prompt_usuario_ss")
async def personalizar_prompt_usuario_ss(data: dict):
    print(f"API Key en uso: {gemini_api_key}")
    try:
        # Extraer el array del JSON
        values = list(data.values())[0]  # Extrae el array contenido en el JSON
        if not isinstance(values, list) or len(values) < 5:
            return {"error": "Formato de datos no válido. El array debe contener al menos 5 elementos."}
        id_usuario, titulo, tipo_personal, pregunta, eleccion = values[:5]
        if not id_usuario or not isinstance(id_usuario, str) or not id_usuario.isalnum():
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
        ##################################EDITADO############
        #Configuracion de la API google Places:
        load_dotenv(dotenv_path="../credenciales.env")
        google_places = os.getenv("GPLACES_API_KEY")
        os.environ["GPLACES_API_KEY"] = google_places
        # Crear instancia de GooglePlacesTool
        places = GooglePlacesTool()
        # Realizar la búsqueda
        try:
            prompt_maps = f"Centros vih " + provincia
            respuesta_google_maps_2 = places.run(prompt_maps)
            pattern = re.compile(r"(\d+)\.\s*(.*?)\nAddress:\s*(.*?)\nGoogle place ID:\s*(.*?)\nPhone:\s*(.*?)\nWebsite:\s*(.*?)\n", re.DOTALL)
            matches = pattern.findall(respuesta_google_maps_2)

            matches = list({match[0]: match for match in matches}.values())

            matches = matches[:3]  # Muestra solo los primeros 3 resultados

            locations_str = ""
            for match in matches:
                location_info = (
                    f"ID: {int(match[0])}\n"
                    f"Name: {match[1].strip()}\n"
                    f"Address: {match[2].strip()}\n"
                    f"Phone: {match[4].strip() if match[4].strip() != 'Unknown' else 'N/A'}\n"
                    f"Website: {match[5].strip() if match[5].strip() != 'Unknown' else 'N/A'}\n"
                    f"{'-' * 40}\n"  # Separador entre cada ubicación
                )
                locations_str += location_info

            # Imprimir el resultado en consola
            print(locations_str)
            print(provincia)
        except Exception as e:
            print(f"Hubo un error al realizar la búsqueda: {e}")
        #######################################################
        prompt = (
            f"Trátame de usted y conjuga los adjetivos en neutro. (Ej: 'Informade, interesade'). No hace falta que me saludes."
            f"Vivo en {provincia}. Dame respuestas orientadas a ese lugar.\n"
            f"Soy personal sanitario y trabajo en este ámbito laboral: {ambito_laboral}.\n"
            f"Estoy trabajando actualmente con vih (úsalo siempre en minúscula). Necesito información profesional sobre {eleccion}."
        )
        respuesta_chatbot = generar_respuesta(prompt)
### GUARDAR CONSULTAS Y EL ARBOL DE CHAT
        raw_data = data["data"]
        respuesta_chatbot = generar_respuesta(prompt)
        # Query adaptada
        query = """INSERT INTO respuestas_chatbot_sanitarios
        (id_usuario, especialidad, recursos)
        VALUES (%s, %s, %s)"""
        # Asignar los datos a los placeholders
        datos_ss = (
            raw_data[0], raw_data[2], raw_data[4])
        # Aquí iría la ejecución en tu conexión a la base de datos
        cursor.execute(query, datos_ss)
        connection.commit()
        query = ''' INSERT INTO respuestas_modelo (id_usuario, respuesta_modelo)
                        VALUES (%s, %s);'''
        valores = (id_usuario, respuesta_chatbot)
        cursor.execute(query, valores)
        connection.commit()
        cursor.close()
        connection.close()
        print("Datos insertados correctamente.")
        ########LOQUE HE AÑADIDO########
        respuesta_final_2 = respuesta_chatbot + respuesta_google_maps_2
        ################################
        return {"respuesta_chatbot": respuesta_final_2}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        except:
            print("Error cerrando la conexión.")


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
#       "titulo": "Tengo vih",
#       "preguntas": {
#         "¿Cuándo te diagnosticaron?": ["Hace menos de 6 meses"],
#         "¿Estás en tratamiento TAR?": ["Sí"],
#         "¿Tienes acceso a un médico?": ["Sí"],
#         "¿Quieres información sobre algún tema?": ["Apoyo psicológico"]
#       }
#     }
#   }
# }

# NO SOCIOSANITARIO
# { "data" : [
#     "1234abcd",
#     "¿Cuál es tu situación?",
#     "Tengo vih",
#     "¿Cuándo te diagnosticaron?",
#     "Hace menos de 6 meses",
#     "¿Estás en tratamiento TAR?",
#     "Sí",
#     "¿Tienes acceso a un médico?",
#     "Sí",
#     "¿Quieres información sobre algún tema?",
#     "Sí",
#     "¿Sabes qué es la PEP?",
#     "Apoyo psicológico"
# ]}
# SOCIOSANITARIO
# {"data" :[
#     "789abc",
#     "Especialidad",
#     "Personal sanitario",
#     "¿Qué necesitas como personal sanitario?",
#     "Manejo clínico de pacientes con vih"
# ]}