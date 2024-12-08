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
            # print(df.head(50))  # Imprime las primeras filas para depuración

    except psycopg2.OperationalError as e:
        raise HTTPException(status_code=400, detail="Error de conexión: " + str(e))
    except Exception as error:
        raise HTTPException(status_code=400, detail="Error desconocido: " + str(error))
    
    
    
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

    df = pd.read_sql_query(query_usuarios, connection)

    json_data = df.to_dict(orient="records")
    
    connection.close()


    return json_data

# # 0.Ruta para obtener todos los libros
# @app.get("/books")
# async def get_books():
#     cursor.execute("SELECT * FROM books")
#     results = cursor.fetchall()
#     return dict({"results":results})