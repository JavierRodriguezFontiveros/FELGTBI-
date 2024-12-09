from prompt_basico import prompt_basico
from fastapi import FastAPI, Query #Api
import uvicorn #Despliegue en Local

import pandas as pd

from fastapi.responses import StreamingResponse
import io
import matplotlib.pyplot as plt

from graficas import crear_grafico_pie, barras_apiladas_genero_orientacion, graficar_permiso_residencia, graficar_combinaciones, buscar_ciudad, obtener_top_5_ciudades, graficar_especialidad
from repo.FELGTBI_plus.backend.utils.utils_connexion import connect_to_db
from repo.FELGTBI_plus.backend.utils.utils_database import fetch_all_from_table


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
class UserData(BaseModel):
    data: Dict[str, Any]

import concurrent.futures

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

                id_usuario = next((seccion.get("id_usuario") for _, seccion in user_data.data.items()), None)
                    
            # Conectar a la base de datos
                connection = connect_to_db()

                if connection is None:
                    return {"error": "No se pudo conectar a la base de datos."}

                try:
                    # Escribir la consulta SQL para obtener los datos
                    query = """
                        SELECT provincia, pronombre_elle, pronombre_el, pronombre_ella
                        FROM no_sociosanit_formulario
                        WHERE id_usuario = %s
                    """

                    # Usar pandas para ejecutar la consulta y convertirla en un DataFrame
                    df = pd.read_sql_query(query, connection, params=(id_usuario,))

                    # Cerrar la conexión después de obtener los datos
                    connection.close()

                except Exception as e:
                    return {"error": f"Ocurrió un error al procesar la solicitud: {e}"}
    ## Extraer datos necesarios del df
                resultados = df.to_dict(orient="records")[0]
                provincia = resultados["provincia"]
                pronombres = []

                if resultados["pronombre_el"]:
                    pronombres.append("Él")
                if resultados["pronombre_ella"]:
                    pronombres.append("Ella")
                if resultados["pronombre_elle"]:
                    pronombres.append("Elle/Pronombre neutro")

                pronombres = ", ".join(pronombres)

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
                    
# SI ES SOCIOSANITARIO
            elif key.startswith("2"):
                #EXTRAER ID_USUARIO
                id_usuario = None

                id_usuario = next((seccion.get("id_usuario") for _, seccion in user_data.data.items()), None)
                    
            # Conectar a la base de datos
                connection = connect_to_db()

                if connection is None:
                    return {"error": "No se pudo conectar a la base de datos."}

                try:
                    # Escribir la consulta SQL para obtener los datos
                    query = """
                        SELECT ambito_laboral, provincia
                        FROM sociosanit_formulario
                        WHERE id_usuario = %s
                    """

                    # Usar pandas para ejecutar la consulta y convertirla en un DataFrame
                    df = pd.read_sql_query(query, connection, params=(id_usuario,))

                    # Cerrar la conexión después de obtener los datos
                    connection.close()

                except Exception as e:
                    return {"error": f"Ocurrió un error al procesar la solicitud: {e}"}
    ## Extraer datos necesarios del df
                resultados = df.to_dict(orient="records")[0]
                provincia = resultados["provincia"]
                ambito_laboral = resultados["ambito_laboral"]

                if key.startswith("2.1"):
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
    