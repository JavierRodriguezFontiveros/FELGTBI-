# Bibliotecas:

from fastapi import FastAPI, Query #Api
import uvicorn #Despliegue en Local

import pandas as pd

from fastapi.responses import StreamingResponse
import io
import matplotlib.pyplot as plt

from graficas import crear_grafico_pie, barras_apiladas_genero_orientacion, graficar_permiso_residencia, graficar_combinaciones, buscar_ciudad, obtener_top_5_ciudades, graficar_especialidad, prueba
from utils_connexion import connect_to_db


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

# Configurar renderer
pio.renderers.default = "browser"
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#CREAR API Y CONFIGURAR MODELO
app = FastAPI()
load_dotenv()




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
        query = "SELECT * FROM sociosanitarios_formulario"  # Cambia la consulta según sea necesario
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
        query = "SELECT * FROM sociosanitarios_formulario"  # Cambia la consulta según sea necesario
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
        query = "SELECT * FROM sociosanitarios_formulario"  # Cambia la consulta según sea necesario

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















    


@app.get("/prueba/", response_class=HTMLResponse)
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

        # Exportar el gráfico como HTML
        html_content = fig.to_html(full_html=False)  # Genera solo el cuerpo del HTML

        # Devolver el HTML como respuesta
        return HTMLResponse(content=html_content, media_type="text/html")
    
    except Exception as e:
        return {"error": f"Ocurrió un error al procesar el gráfico: {e}"}

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
        
        # # json_data = df.to_dict(orient="records")
        # json_data = json.dumps(result, indent=3, ensure_ascii=False)
        
        # print(json_data)
        
        connection.close()

        return result
    
    except Exception as e:
        return {"error": f"Ha ocurrido algún problema obteniendo las preguntas: {e}"}








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
