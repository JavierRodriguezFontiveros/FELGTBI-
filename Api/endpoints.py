from fastapi import FastAPI, requests, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
import psycopg2
import json
import pandas as pd

app = FastAPI()


load_dotenv()
    
#Leer Las Variables:
host = os.getenv("DB_HOST_AWS")
username = os.getenv("DB_USER_AWS")
password = os.getenv("DB_PASSWORD_AWS")
database = os.getenv("DB_DATABASE_AWS")
port = os.getenv("DB_PORT_AWS")

# class Book(BaseModel):
#     published: int
#     author: str
#     title: str
#     first_sentence: str



@app.get("/preguntas_user/")
async def preguntas_user():  
    # Establecer la conexión
    try:
        connection = psycopg2.connect(host=host,
                                    database=database,
                                    user=username,
                                    password=password,
                                    port=port,
                                    sslmode="require")
        
        print("Conexión exitosa a la base de datos PostgreSQL con SSL")

    except psycopg2.OperationalError as e:
        raise HTTPException(status_code=400, detail="Error de conexión: " + str(e))
    except Exception as error:
        raise HTTPException(status_code=400, detail="Error desconocido: " + str(e))
    
    # Escribe la consulta SQL
    query = "SELECT * FROM sociosanitarios_data"
    
    # Usa pandas para ejecutar la consulta y convertirla en un DataFrame
    df = pd.read_sql_query(query, connection)
    
    # Agrupar opciones por pregunta y categoría
    grouped = df.groupby(["id_categoria", "titulo_categoria", "texto_pregunta"])["texto_opcion"].apply(list).reset_index()

    # Crear el JSON dinámico
    json_data = {}
    for _, row in grouped.iterrows():
        id_categoria = row["id_categoria"]
        titulo = row["titulo_categoria"]
        pregunta = row["texto_pregunta"]
        opciones = row["texto_opcion"]
        
        if id_categoria not in json_data:
            json_data[id_categoria] = {"titulo": titulo, "preguntas": {}}
        
        json_data[id_categoria]["preguntas"][pregunta] = opciones

    # Convertir a JSON
    json_resultado = json.dumps(json_data, indent=4, ensure_ascii=False)

    print(json_resultado)

    return json_resultado

# # 0.Ruta para obtener todos los libros
# @app.get("/books")
# async def get_books():
#     cursor.execute("SELECT * FROM books")
#     results = cursor.fetchall()
#     return dict({"results":results})