
from fastapi import FastAPI, HTTPException
import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()

# Obtener las claves
db_host = os.getenv("DB_HOST_AWS")
db_username = os.getenv("DB_USER_AWS")
db_password = os.getenv("DB_PASSWORD_AWS")
db_database = os.getenv("DB_DATABASE_AWS")
db_port = int(os.getenv("DB_PORT_AWS", 5432))

# Conectar con la bbdd
conn = psycopg2.connect(database = db_database, 
                        user = db_username, 
                        host= db_host,
                        password = db_password,
                        port = db_port)

# Generamos un cursor para operar dentro de la bbdd
cur = conn.cursor()



#function to retrieve all data
def fetch_all_from_table(table_name: str) -> dict:
    valid_tables = {"categorias_chatbot", "preguntas_chatbot", "opciones_chatbot"}
    if table_name not in valid_tables:
        raise ValueError("Invalid table name provided.")

    try:
        query = f"SELECT * FROM {table_name};"
        cur.execute(query) #cur. aleady defined GLOBALLY in main script
        rows = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        # Convert rows into a list of dictionaries
        return [dict(zip(column_names, row)) for row in rows]
    except Exception as e:
        raise RuntimeError(f"Error fetching data: {e}")


#fastapi CHAT data retrieval endpoint 
app = FastAPI()

@app.get("/get-table/{table_name}")
def get_table_data(table_name: str):
    try:
        data = fetch_all_from_table(cur, table_name)
        return {"table_name": table_name, "data": data}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == '__main__':
    print(fetch_all_from_table('opciones_chatbot'))

