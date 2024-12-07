from fastapi import FastAPI, requests, HTTPException
import uvicorn
import os
from dotenv import load_dotenv
import psycopg2
import json
import pandas as pd


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


app = FastAPI()

@app.get("/preguntas_user/")
async def preguntas_user():  
    try:
        # Usar contexto para gestionar la conexión
        with psycopg2.connect(
            host=host,
            database=database,
            user=username,
            password=password,
            port=port,
            sslmode="require"
        ) as connection:
            print("Conexión exitosa a la base de datos PostgreSQL con SSL")

            # Escribe la consulta SQL
            query = "SELECT * FROM preguntas_front"

            # Usa pandas para ejecutar la consulta y convertirla en un DataFrame
            df = pd.read_sql_query(query, connection)
            print(df.head(50))  # Imprime las primeras filas para depuración

    except psycopg2.OperationalError as e:
        raise HTTPException(status_code=400, detail="Error de conexión: " + str(e))
    except Exception as error:
        raise HTTPException(status_code=400, detail="Error desconocido: " + str(error))
    
    
    
    # Agrupar opciones por pregunta y categoría
    grouped = (
        df.groupby(["id_categoria", "titulo_categoria", "texto_pregunta"])["texto_opcion"]
        .apply(list)
        .reset_index()
    )

    # Crear el JSON dinámico
    json_data = {}
    for _, row in grouped.iterrows():
        id_categoria = row["id_categoria"]
        titulo = row["titulo_categoria"]
        pregunta = row["texto_pregunta"]
        opciones = row["texto_opcion"]

        # Crear la estructura del JSON
        if id_categoria not in json_data:
            json_data[id_categoria] = {"titulo": titulo, "preguntas": {}}

        json_data[id_categoria]["preguntas"][pregunta] = opciones

    # Convertir a JSON
    json_resultado = json.dumps(json_data, indent=4, ensure_ascii=False)

    # Imprimir el JSON resultante
    print(json_resultado)


    return json_resultado

# # 0.Ruta para obtener todos los libros
# @app.get("/books")
# async def get_books():
#     cursor.execute("SELECT * FROM books")
#     results = cursor.fetchall()
#     return dict({"results":results})