
import psycopg2
import os
from dotenv import load_dotenv

def connect_to_db():
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv()
    
    # Configura los parámetros de la conexión
    db_host = os.getenv("DB_HOST_AWS")
    db_username = os.getenv("DB_USER_AWS")
    db_password = os.getenv("DB_PASSWORD_AWS")
    db_database = os.getenv("DB_DATABASE_AWS")
    db_port = int(os.getenv("DB_PORT_AWS", 5432))

    # Establecer la conexión
    try:
        connection = psycopg2.connect(host=db_host,
                                      database=db_database,
                                      user=db_username,
                                      password=db_password,
                                      port=db_port,
                                      sslmode="require")
        
        print("Conexión exitosa a la base de datos PostgreSQL con SSL")
        return connection  
    
    except psycopg2.OperationalError as e:
        print("Error de conexión:", e)
        return None  
    
    except Exception as error:
        print("Error desconocido:", error)
        return None  
    


import plotly.express as px

def crear_grafico_pie(dataframe, viven_espana=True):
    # Filtro para el DataFrame
    filtro = dataframe['vives_espana'] == viven_espana
    df_filtrado = dataframe[filtro]
    
    # Conteo de orientaciones
    colectivos_count = df_filtrado['orientacion'].value_counts().reset_index()
    colectivos_count.columns = ['Orientacion', 'Cantidad']
    
    # Tener en cuenta ambas posibilidades
    titulo = "Distribución de Orientación Sexual"
    if viven_espana:
        titulo += " (Personas que Viven en España)"
    else:
        titulo += " (Personas que No Viven en España)"
    
    # Crear gráfico de pastel
    fig = px.pie(colectivos_count, 
                 values='Cantidad', 
                 names='Orientacion', 
                 title=titulo,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    
    return fig

