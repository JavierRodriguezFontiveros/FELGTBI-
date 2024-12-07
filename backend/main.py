# Bibliotecas:
from fastapi import FastAPI, Query #Api
import uvicorn #Despliegue en Local

import pandas as pd

from fastapi.responses import StreamingResponse
import io
import matplotlib.pyplot as plt

from graficas import crear_grafico_pie, barras_apiladas_genero_orientacion, graficar_permiso_residencia, graficar_combinaciones, buscar_ciudad, obtener_top_5_ciudades, graficar_especialidad
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
try:
    gemini_api_key = load_dotenv()
    
    if not gemini_api_key:
        raise ValueError("La variable GEMINI_API_KEY no está definida. Verifica tu archivo .env o las variables de entorno.")
    
    genai.configure(api_key=gemini_api_key)
    print("API configurada correctamente con la clave proporcionada.")

except Exception as e:
    print(f"Error al configurar la API: {e}")
    raise


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
        query = "SELECT * FROM user_data"  # Cambia esta consulta según sea necesario

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
        query = "SELECT * FROM user_data"  # Cambia esta consulta según sea necesario

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
        query = "SELECT * FROM user_data"  # Cambia esta consulta según sea necesario

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
        query = "SELECT * FROM user_data"  # Cambia esta consulta según sea necesario

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
        query = "SELECT * FROM user_data"  # Cambia esta consulta según sea necesario

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
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
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
pronombres= "Elle"
ambito_laboral = "Centro social2"


class UserData(BaseModel):
    data: Dict[str, Any]

def generar_respuesta(prompt):
    try:
        print(f"Llamando al modelo con prompt: {prompt}")
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt, timeout=30)
        print("Respuesta generada con éxito.")
        if not response or not hasattr(response, 'text'):
            raise ValueError("Respuesta vacía o no válida del modelo.")
        return response.text
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
                prompt = ("Mis prnombres son:" + pronombres + ". \n"
                        "Vivo en" + provincia + ". \n"
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
                prompt = ("Mis prnombres son:" + pronombres + ". \n"
                        "Vivo en" + provincia + ". \n"
                        "Creo que me he expuesto al virus en " + tiempo_exposicion + ". \n"
                        "El tipo de exposición ha sido:" + tipo_exposicion + ". \n"
                        + chem_sex + "ha sido en entorno de chem-sex. \n"
                        "He compartido mi preocupación con"+ preocupacion + "Y quiero más información sobre la PEP."
                )

            elif key.startswith("1.3"):
                tema_informacion = preguntas.get("¿Sobre qué tema quieres información?", [" "])[0]

                # Crear el prompt para la sección 1.3
                prompt = ("Quiero información sobre:" + tema_informacion)

            elif key.startswith("1.4"):
                acceso_grupos = preguntas.get("¿Tienes acceso a recursos locales o grupos de apoyo?", [" "])[0]
                preocupacion4 = preguntas.get("¿Has compartido tu preocupación con alguien?", [" "])[0]
                apoyo_necesario = preguntas.get("¿Qué apoyo necesitas?", [" "])[0]

                # Crear el prompt para la sección 1.4
                prompt = ("Estoy acompañando a una persona seropositiva." + acceso_grupos + "tengo acceso a recursos locales o grupos de apoyo. /n"
                        "He compartido mi preocupación con" + preocupacion4 + ". /n"
                        "Me gustaría orientación para conseguir" + apoyo_necesario)
                
            elif key.startswith("2.1"):
                eleccion = preguntas.get("¿Qué necesitas?", [" "])[0]

                # Crear el prompt para la sección 2.1
                prompt = ("Soy personal sanitario y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                        "Necesito información sobre" + eleccion + ".")
                
            elif key.startswith("2.2"):
                eleccion2 = preguntas.get("¿Qué necesitas?", [" "])[0]

                # Crear el prompt para la sección 2.1
                prompt = ("Soy trabajador social y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                        "Necesito información sobre" + eleccion2 + ".")

            elif key.startswith("2.3"):
                eleccion3 = preguntas.get("¿Qué necesitas?", [" "])[0]

                # Crear el prompt para la sección 2.1
                prompt = ("Soy psicólogo y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                        "Necesito información sobre" + eleccion3 + ".")
                
            elif key.startswith("2.4"):
                eleccion4 = preguntas.get("¿Qué necesitas?", [" "])[0]

                # Crear el prompt para la sección 2.1
                prompt = ("Soy educador y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                        "Necesito información sobre" + eleccion4 + ".")
                
            elif key.startswith("2.5"):
                eleccion5 = preguntas.get("¿Qué necesitas?", [" "])[0]

                # Crear el prompt para la sección 2.1
                prompt = ("Soy voluntario/cuidador y trabajo en este ámbito laboral:" + ambito_laboral + ". /n"
                        "Necesito información sobre" + eleccion5 + ".")

            else:
                prompt = "Título: "

            # Generar la respuesta del modelo
            respuesta_chatbot = generar_respuesta(prompt)

            # Devolver la respuesta del chatbot
            return {"respuesta_chatbot": respuesta_chatbot}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

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
