# Bibliotecas:
from prompt_basico import prompt_basico
from fastapi import FastAPI, Query #Api
import uvicorn #Despliegue en Local

import pandas as pd

from fastapi.responses import StreamingResponse
import io
import matplotlib.pyplot as plt

from graficas import crear_grafico_pie, barras_apiladas_genero_orientacion, graficar_permiso_residencia, graficar_combinaciones, buscar_ciudad, obtener_top_5_ciudades, graficar_especialidad, prueba
from utils import connect_to_db

from io import BytesIO

from fastapi.responses import JSONResponse

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv
import os

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
@app.get("/")
async def home():
    return {"message": """
Hola buenas bienvenido a este proyecto de tripulaciones
                   """}




''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/bar-chart/")
def generate_bar_chart():
    # Conectar a la base de datos
    connection = connect_to_db()

    if connection is None:
        return {"error": "No se pudo conectar a la base de datos."}
    
    try:
        # Escribir la consulta SQL para obtener los datos
        query = "SELECT * FROM no_sociosanit_formulario"  # Cambia esta consulta según sea necesario

        # Usar pandas para ejecutar la consulta y convertirla en un DataFrame
        df = pd.read_sql_query(query, connection)

        # Cerrar la conexión después de obtener los datos
        connection.close()

        # Definir los rangos de edades y las etiquetas correspondientes
        bins = [0, 15, 19, 24, 29, 39, 49, 59, 100]
        labels = ['Menores de 16', 'Adolescentes (15-19)', 'Jóvenes adultos (20-24)', 
                  'Adultos jóvenes (25-29)', 'Adultos en plena madurez (30-39)', 
                  'Adultos maduros (40-49)', 'Adultos mayores (50-59)', 'Mayores de 60']

        # Asegurarse de que la columna 'edad' está en formato numérico
        df['edad'] = pd.to_numeric(df['edad'], errors='coerce')

        # Crear una nueva columna 'grupo_edad' con las categorías de edad
        df['grupo_edad'] = pd.cut(df['edad'], bins=bins, labels=labels, right=False)

        # Contar la cantidad de personas en cada grupo de edad
        edad_grupo = df.groupby('grupo_edad').size().reset_index(name='cantidad')

        # Crear el gráfico de barras
        plt.figure(figsize=(10, 6))
        plt.bar(edad_grupo['grupo_edad'], edad_grupo['cantidad'], color="blue", alpha=0.7)
        plt.title("Distribución de Edad por Grupo")
        plt.xlabel("Grupo de Edad")
        plt.ylabel("Cantidad de Personas")
        plt.xticks(rotation=45, ha='right')  # Rotar las etiquetas del eje X

        # Guardar el gráfico en un buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        plt.close()

        # Devolver el gráfico como una respuesta de imagen
        return StreamingResponse(buf, media_type="image/png")

    except Exception as e:
        return {"error": f"Ocurrió un error al procesar los datos: {e}"}



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/grafico-pie/")
def generar_grafico_pie(viven_espana: bool = True):
    connection = connect_to_db()
    try:
        # Escribir la consulta SQL para obtener los datos
        query = "SELECT * FROM no_sociosanit_formulario"  # Cambia esta consulta según sea necesario

        # Usar pandas para ejecutar la consulta y convertirla en un DataFrame
        df = pd.read_sql_query(query, connection)

        # Cerrar la conexión después de obtener los datos
        connection.close()
        
        # Crear el gráfico de pastel
        fig = crear_grafico_pie(df, viven_espana)

        # Guardar el gráfico como imagen en un buffer
        img_bytes = fig.to_image(format="png")

        # Crear un buffer de memoria
        buf = BytesIO(img_bytes)
        buf.seek(0)

        # Devolver la imagen como respuesta
        return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}
    


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/barras-apiladas/")
def generar_barras_apiladas():
    connection = connect_to_db()
    try:
        # Escribir la consulta SQL para obtener los datos
        query = "SELECT * FROM no_sociosanit_formulario"  # Cambia esta consulta según sea necesario

        # Usar pandas para ejecutar la consulta y convertirla en un DataFrame
        df = pd.read_sql_query(query, connection)

        # Cerrar la conexión después de obtener los datos
        connection.close()

        # Generar el gráfico de barras apiladas
        fig = barras_apiladas_genero_orientacion(df)

        # Guardar el gráfico como imagen en un buffer
        img_bytes = fig.to_image(format="png")

        # Crear un buffer de memoria
        buf = BytesIO(img_bytes)
        buf.seek(0)

        # Devolver la imagen como respuesta
        return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}
    


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/grafico-permiso-residencia/")
def generar_grafico_permiso_residencia():
    connection = connect_to_db()
    try:
        # Escribir la consulta SQL para obtener los datos
        query = "SELECT * FROM no_sociosanit_formulario"  # Cambia esta consulta según sea necesario

        # Usar pandas para ejecutar la consulta y convertirla en un DataFrame
        df = pd.read_sql_query(query, connection)

        # Cerrar la conexión después de obtener los datos
        connection.close()

        # Generar el gráfico de permisos de residencia
        fig = graficar_permiso_residencia(df)

        # Guardar el gráfico como imagen en un buffer
        img_bytes = fig.to_image(format="png")

        # Crear un buffer de memoria
        buf = BytesIO(img_bytes)
        buf.seek(0)

        # Devolver la imagen como respuesta
        return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}
    


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/grafico-combinaciones/")
def generar_grafico_combinaciones():
    connection = connect_to_db()
    try:
        # Escribir la consulta SQL para obtener los datos
        query = "SELECT * FROM no_sociosanit_formulario"  # Cambia esta consulta según sea necesario

        # Usar pandas para ejecutar la consulta y convertirla en un DataFrame
        df = pd.read_sql_query(query, connection)

        # Cerrar la conexión después de obtener los datos
        connection.close()

        # Generar el gráfico de combinaciones
        fig = graficar_combinaciones(df)

        # Guardar el gráfico como imagen en un buffer
        img_bytes = fig.to_image(format="png")

        # Crear un buffer de memoria
        buf = BytesIO(img_bytes)
        buf.seek(0)

        # Devolver la imagen como respuesta
        return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}
    


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/buscar-ciudad/")
def endpoint_buscar_ciudad(ciudad: str = Query(..., description="Nombre de la ciudad a buscar en la tabla.")):
    connection = connect_to_db()
    try:
        # Obtener datos de la base de datos
        query = "SELECT * FROM sociosanitarios_data"  # Cambia la consulta según sea necesario
        df = pd.read_sql_query(query, connection)
        connection.close()

        # Buscar información de la ciudad
        info_ciudad = buscar_ciudad(df, ciudad)

        # Devolver la respuesta
        return JSONResponse(content=info_ciudad)
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar la solicitud: {e}"}


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/top-5-ciudades/")
def endpoint_top_5_ciudades():
    connection = connect_to_db()
    try:
        # Obtener datos de la base de datos
        query = "SELECT * FROM sociosanitarios_data"  # Cambia la consulta según sea necesario
        df = pd.read_sql_query(query, connection)
        connection.close()

        # Obtener el top 5 de ciudades
        top_5_ciudades = obtener_top_5_ciudades(df)

        # Devolver la respuesta
        return JSONResponse(content={"Top_5_Ciudades": top_5_ciudades})
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar la solicitud: {e}"}
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/grafico-especialidad/")
def generar_grafico_especialidad():
    connection = connect_to_db()
    try:
        # Consulta para obtener los datos
        query = "SELECT * FROM sociosanitarios_data"  # Cambia la consulta según sea necesario

        # Convertir los datos en un DataFrame
        df = pd.read_sql_query(query, connection)

        # Generar el gráfico de especialidades
        fig = graficar_especialidad(df)

        # Guardar el gráfico como imagen en un buffer
        img_bytes = fig.to_image(format="png")

        # Crear un buffer de memoria
        buf = BytesIO(img_bytes)
        buf.seek(0)

        # Devolver la imagen como respuesta
        return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}
    finally:
        connection.close()


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from enum import Enum


class GenderIdentity(str, Enum):
    hombre_cis = "Hombre Cis"
    hombre_trans = "Hombre Trans"
    mujer_cis = "Mujer Cis"
    mujer_trans = "Mujer Trans"
    no_binario = "No binario"
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
    soltero = "Soltero"
    en_pareja = "En pareja"
    casado = "Casado"
    divorciado = "Divorciado"
    viudo = "Viudo"
    otro = "Otro"

class Nacionalidad(str,Enum):
    afghana = "Afghana"
    albanesa = "Albanesa"
    alemana = "Alemana"
    andorrana = "Andorrana"
    angoleña = "Angoleña"
    antigua_y_barbudense = "Antigua y Barbudense"
    argentina = "Argentina"
    armenia = "Armenia"
    australiana = "Australiana"
    austriaca = "Austríaca"
    azerbaiyana = "Azerbaiyana"
    bahameña = "Bahameña"
    bangladesi = "Bangladesí"
    barbadense = "Barbadense"
    bielorrusa = "Bielorrusa"
    belga = "Belga"
    beliceña = "Beliceña"
    beninesa = "Beninesa"
    boliviana = "Boliviana"
    bosnia_y_herzegovina = "Bosnia y Herzegovina"
    botswana = "Botswana"
    brasileña = "Brasileña"
    bruneana = "Bruneana"
    bulgara = "Búlgara"
    burundesa = "Burundesa"
    butanesa = "Butanesa"
    barbuda = "Bárbuda"
    caboverdiana = "Caboverdiana"
    camboyana = "Camboyana"
    camerunesa = "Camerunesa"
    canadiense = "Canadiense"
    chadiana = "Chadiana"
    chilena = "Chilena"
    china = "China"
    chipriota = "Chipriota"
    colombiana = "Colombiana"
    comorense = "Comorense"
    congoleña = "Congoleña"
    costarricense = "Costarricense"
    croata = "Croata"
    cubana = "Cubana"
    danesa = "Danesa"
    dominicana = "Dominicana"
    ecuatoriana = "Ecuatoriana"
    egipcia = "Egipcia"
    emirati = "Emiratí"
    ecuatoguineana = "Ecuatoguineana"
    eslovaca = "Eslovaca"
    eslovena = "Eslovena"
    española = "Española"
    estadounidense = "Estadounidense"
    estonia = "Estonia"
    etiopia = "Etiopía"
    fiyiana = "Fiyiana"
    filipina = "Filipina"
    finlandesa = "Finlandesa"
    francesa = "Francesa"
    gabonesa = "Gabonesa"
    gambiana = "Gambiana"
    georgiana = "Georgiana"
    ghanesa = "Ghanesa"
    granadina = "Granadina"
    guatemalteca = "Guatemalteca"
    guineana = "Guineana"
    guineoecuatoriana = "Guineoecuatoriana"
    guyanes = "Guyanes"
    haitiana = "Haitiana"
    hondureña = "Hondureña"
    hongkonesa = "Hongkonesa"
    hungara = "Hungara"
    icelandeza = "Icelandeza"
    india = "India"
    indonesa = "Indonesa"
    iraki = "Irakí"
    irani = "Iraní"
    israeli = "Israelí"
    italiana = "Italiana"
    jamaicana = "Jamaicana"
    japonera = "Japonera"
    jordana = "Jordana"
    keniana = "Keniana"
    kirguisa = "Kirguisa"
    kosovar = "Kosovar"
    kuwaiti = "Kuwaiti"
    laosiana = "Laosiana"
    latviana = "Latviana"
    lesotense = "Lesotense"
    liberiana = "Liberiana"
    libia = "Libia"
    liechtensteiniana = "Liechtensteiniana"
    lituana = "Lituana"
    luxemburguesa = "Luxemburguesa"
    macedonia = "Macedonia"
    madagascariana = "Madagascariana"
    malagueña = "Malagueña"
    malawiana = "Malawiana"
    malasia = "Malasia"
    maldiva = "Maldiva"
    maliense = "Maliense"
    marfileña = "Marfileña"
    mauriciana = "Mauriciana"
    mauritana = "Mauritana"
    mexicana = "Mexicana"
    mianmara = "Mianmara"
    moldava = "Moldava"
    monegasca = "Monegasca"
    mongola = "Mongola"
    mozambiqueña = "Mozambiqueña"
    namibia = "Namibia"
    nauruana = "Nauruana"
    nepalesa = "Nepalesa"
    nicaragüense = "Nicaragüense"
    nigeriana = "Nigeriana"
    noruega = "Noruega"
    nueva_zelanda = "Nueva Zelanda"
    niger = "Níger"
    palestina = "Palestina"
    panameña = "Panameña"
    papua_nueva_guinea = "Papúa Nueva Guinea"
    paraguaya = "Paraguaya"
    peruana = "Peruana"
    polaca = "Polaca"
    portuguesa = "Portuguesa"
    qatari = "Qatarí"
    reino_unido = "Reino Unido"
    republica_checa = "República Checa"
    republica_dominicana = "República Dominicana"
    ruandesa = "Ruandesa"
    rumana = "Rumana"
    rusa = "Rusa"
    salvadoreña = "Salvadoreña"
    samoana = "Samoana"
    san_cristobal_y_nieves = "San Cristóbal y Nieves"
    san_marino = "San Marino"
    sao_tomeana = "Sao Tomeana"
    senegalesa = "Senegalesa"
    serbia = "Serbia"
    seychelense = "Seychelense"
    sierra_leona = "Sierra Leona"
    singapurense = "Singapurense"
    siria = "Siria"
    somali = "Somalí"
    sri_lanka = "Sri Lanka"
    sudafricana = "Sudafricana"
    sudanesa = "Sudanesa"
    surinamesa = "Surinamesa"
    sueca = "Sueca"
    suiza = "Suiza"
    sudano = "Súdano"
    svajilandesa = "Svajilandesa"
    tailandesa = "Tailandesa"
    tanzana = "Tanzana"
    togo = "Togo"
    tonga = "Tonga"
    trinitaria_y_tobaguense = "Trinitaria y Tobaguense"
    tunisina = "Tunisina"
    turca = "Turca"
    turcomana = "Turcomana"
    tuvalu = "Tuvalu"
    ucraniana = "Ucraniana"
    ugandesa = "Ugandesa"
    uruguaya = "Uruguaya"
    uzbeca = "Uzbeca"
    vanuatu = "Vanuatu"
    venezolana = "Venezolana"
    vietnamita = "Vietnamita"
    yemeni = "Yemení"
    yugoslava = "Yugoslava"
    zambiana = "Zambiana"
    zimbabuense = "Zimbabuense"

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
    edad: int

    pronombre_el: bool  
    pronombre_ella: bool  
    pronombre_elle: bool  

    identidad_genero: GenderIdentity
    orientacion_sexual: SexualOrientation
    vives_en_espana: bool
    pais: Nacionalidad  
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
                                                orientacion_sexual, vives_en_espana, pais, permiso_residencia,
                                                persona_racializada, persona_discapacitada, persona_sin_hogar,
                                                persona_migrante, persona_intersexual, nivel_estudios, situacion_afectiva,
                                                provincia)
           VALUES (%(edad)s, %(pronombre_el)s, %(pronombre_ella)s, %(pronombre_elle)s, %(identidad_genero)s,
                   %(orientacion_sexual)s, %(vives_en_espana)s, %(pais)s, %(permiso_residencia)s,
                   %(persona_racializada)s, %(persona_discapacitada)s, %(persona_sin_hogar)s, %(persona_migrante)s,
                   %(persona_intersexual)s, %(nivel_estudios)s, %(situacion_afectiva)s, %(provincia)s)
    """
    
    data = {
            "edad": user_data.edad,
            "pronombre_el": user_data.pronombre_el,
            "pronombre_ella": user_data.pronombre_ella,
            "pronombre_elle": user_data.pronombre_elle,
            "identidad_genero": user_data.identidad_genero,
            "orientacion_sexual": user_data.orientacion_sexual,
            "vives_en_espana": user_data.vives_en_espana,
            "pais": user_data.pais,
            "permiso_residencia": user_data.permiso_residencia,
            "persona_racializada": user_data.persona_racializada,
            "persona_discapacitada": user_data.persona_discapacitada,
            "persona_sin_hogar": user_data.persona_sin_hogar,
            "persona_migrante": user_data.persona_migrante,
            "persona_intersexual": user_data.persona_intersexual,
            "nivel_estudios": user_data.nivel_estudios,
            "situacion_afectiva": user_data.situacion_afectiva,
            "provincia": user_data.provincia,
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
    centro_salud = "Centro de Salud"
    hospital = "Hospital"
    centro_comunitario = "Centro comunitario"
    consulta_privada = "Consulta privada"
    asociacion = "Asociación"
    otro = "Otro"

class SociosanitaryData(BaseModel):
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
                                                    ambito_laboral)
           VALUES (%(provincia)s, %(ambito_laboral)s)
    """
    
    data = {
            "provincia": sociosanitary_data.provincia,
            "ambito_laboral": sociosanitary_data.ambito_laboral
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

#
#
#
#
# Definir el esquema para la solicitud entrante
# pronombres = seccion.get("pronombres", "")
# provincia = seccion.get("provincia", "")
# ambito_laboral = seccion.get("ambito_laboral", "")
# provincia = seccion.get("provincia", "")
provincia = "Asturias"
pronombres= "Elle, género neutro"
ambito_laboral = "Centro social"

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


@app.post("/personalizar_prompt")
async def personalizar_prompt(user_data: UserData):
    print(f"API Key en uso: {gemini_api_key}")  # Verifica si la clave está accesible aquí
    try:
        # Determinar el tipo de sección y construir el prompt dinámicamente
        for key, seccion in user_data.data.items():
            titulo = seccion.get("titulo", " ")
            preguntas = seccion.get("preguntas", {})

            # Verificar el tipo de sección
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
                
            elif key.startswith("2.1"):
                eleccion = preguntas.get("¿Qué necesitas?", [" "])[0]

                # Crear el prompt para la sección 2.1
                prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                        "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                        "Soy personal sanitario y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                        "Necesito información sobre" + eleccion + ".")
                
            elif key.startswith("2.2"):
                eleccion2 = preguntas.get("¿Qué necesitas?", [" "])[0]

                # Crear el prompt para la sección 2.1
                prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                        "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                        "Soy trabajador social y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                        "Necesito información sobre" + eleccion2 + ".")

            elif key.startswith("2.3"):
                eleccion3 = preguntas.get("¿Qué necesitas?", [" "])[0]

                # Crear el prompt para la sección 2.1
                prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                        "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                        "Soy psicólogo y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                        "Necesito información sobre" + eleccion3 + ".")
                
            elif key.startswith("2.4"):
                eleccion4 = preguntas.get("¿Qué necesitas?", [" "])[0]

                # Crear el prompt para la sección 2.1
                prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                        "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                        "Soy educador y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                        "Necesito información sobre" + eleccion4 + ".")
                
            elif key.startswith("2.5"):
                eleccion5 = preguntas.get("¿Qué necesitas?", [" "])[0]

                # Crear el prompt para la sección 2.1
                prompt = ("Mis pronombres (dirígete a mi conjugando como corresponda, si es elle, en género neutro, si es él/ella, pues en masculino/femenino, si te digo varios, usa solo uno de los que te diga) son:" + pronombres + ". \n"
                        "Vivo en" + provincia + ". Dame respuestas orientadas a ese lugar. \n"
                        "Soy voluntario/cuidador y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                        "Necesito información sobre" + eleccion5 + ".")

            else:
                prompt = "Título: "

            # Generar la respuesta del modelo
            respuesta_chatbot = generar_respuesta(prompt)

            # Devolver la respuesta del chatbot
            return {"respuesta_chatbot": respuesta_chatbot}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/prueba/")
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
        fig = prueba(df, viven_espana)

        # Guardar el gráfico como imagen usando kaleido
        img_bytes = fig.to_image(format="png", engine="kaleido")

        # Crear un buffer de memoria para la imagen
        buf = BytesIO(img_bytes)
        buf.seek(0)

        # Devolver la imagen como respuesta
        return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}







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
#   "error": "Ocurrió un error al procesar el gráfico: \nImage export using the "kaleido" engine requires the kaleido package,\nwhich can be installed using pip:\n    $ pip install -U kaleido\n"
# }




