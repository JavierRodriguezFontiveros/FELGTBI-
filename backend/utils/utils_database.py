from fastapi import FastAPI, HTTPException
import psycopg2
from dotenv import load_dotenv
import os
from repo.FELGTBI_plus.backend.utils.utils_connexion import connect_to_db


conn = connect_to_db()
cur = conn.cursor()



#function to retrieve all data
def fetch_all_from_table(table_name: str) -> dict:
    valid_tables = {"categorias_chatbot", "preguntas_chatbot", "opciones_chatbot"}
    if table_name not in valid_tables:
        raise ValueError("Invalid table name provided.")

    try:
        query = f"SELECT * FROM {table_name};"
        cur.execute(query) 
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        # Convert rows into a list of dictionaries
        return [dict(zip(column_names, row)) for row in rows]
    except Exception as e:
        raise RuntimeError(f"Error fetching data: {e}")