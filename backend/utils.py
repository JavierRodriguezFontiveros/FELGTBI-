import psycopg2
import os
from dotenv import load_dotenv

def connect_to_db():
    # Cargar las variables de entorno desde el archivo .env
    load_dotenv(dotenv_path="../credenciales.env")
    
    # Configura los parámetros de la conexión
    db_host = os.getenv("DB_HOST_AWS")
    db_username = os.getenv("DB_USER_AWS")
    db_password = os.getenv("DB_PASSWORD_AWS")
    db_database = os.getenv("DB_DATABASE_AWS")
    db_port = int(os.getenv("DB_PORT_AWS", 5432))


    print(f"DB Host: {db_host}")
    print(f"DB User: {db_username}")
    print(f"DB Password: {db_password}")
    print(f"DB Database: {db_database}")
    print(f"DB Port: {db_port}")

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


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



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
    

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


prompt_basico = (
    "Eres un experto sociosanitario especializado en vih y sida. "
    "Siempre que escribas 'vih', lo haces en minúscula, sin excepción. "
    "Trabajas en la FELGTBI+ (Federación Estatal LGTBI+) y ofreces respuestas extensas, detalladas y útiles, basadas en: "
    "1. Recursos concretos (direcciones físicas, teléfonos, correos electrónicos y sitios web). "
    "2. Servicios disponibles que pueda ofrecer la FELGTBI+ o recursos externos cuando la Federación no pueda cubrir la necesidad. "
    "Prioriza recursos presenciales en la provincia donde vive quien pregunta. Si no los encuentras, proporciona opciones telefónicas o virtuales de otros lugares. "
    "Respondes con compasión, cercanía y profesionalismo, en un lenguaje claro, accesible y no técnico. "
    "Siempre remites a tu lugar de trabajo y sus datos de contacto: "
    "FELGTBI+ (Federación Estatal LGTBI+), Teléfono: 91 360 46 05, Correo electrónico: info@felgtbi.org, Sitio web: https://felgtbi.org/. "
    "Importante: Investiga en internet recursos concretos cuando sea necesario y nunca inventes información."
)




''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import plotly.io as pio
import plotly.express as px


# Configurar renderer
pio.renderers.default = "svg"

def crear_grafico_pie(dataframe, viven_espana=True):
    # Filtro para el DataFrame
    filtro = dataframe['vives_en_espana'] == viven_espana
    df_filtrado = dataframe[filtro]
    
    # Conteo de orientaciones
    colectivos_count = df_filtrado['orientacion_sexual'].value_counts().reset_index()
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



def barras_apiladas_genero_orientacion(dataframe):
    # Agrupar y contar las combinaciones de género y orientación
    datos_agrupados = dataframe.groupby(['identidad_genero', 'orientacion_sexual']).size().reset_index(name='Cantidad')

    # Configurar el gráfico de barras apiladas
    fig = px.bar(datos_agrupados,
                 x='identidad_genero',
                 y='Cantidad',
                 color='orientacion_sexual',
                 title='Distribución de Género y Orientación Sexual',
                 labels={'identidad_genero': 'Género', 'orientacion_sexual': 'Orientación Sexual'},
                 barmode='stack',  
                 color_discrete_sequence=px.colors.qualitative.Pastel)

    return fig

def graficar_permiso_residencia(dataframe):
    # Contar las frecuencias de los valores en la columna 'permiso_residencia'
    permiso_count = dataframe['permiso_residencia'].value_counts().reset_index()
    permiso_count.columns = ['Permiso de Residencia', 'Cantidad']
    
    # Calcular los porcentajes
    total = permiso_count['Cantidad'].sum()
    permiso_count['Porcentaje'] = (permiso_count['Cantidad'] / total) * 100
    
    # Calcular el índice de la sección con el valor más grande
    max_value_index = permiso_count['Cantidad'].idxmax()
    
    # Crear un vector donde la porción con el valor más grande será destacada
    pull_values = [0 if i != max_value_index else 0.1 for i in range(len(permiso_count))]
    
    # Crear gráfico de pastel (pie chart) con cantidades y porcentajes
    fig = px.pie(permiso_count, 
                 names='Permiso de Residencia', 
                 values='Cantidad', 
                 title='Distribución de Permisos de Residencia',
                 labels={'Permiso de Residencia': 'Tipo de Permiso'},
                 color='Permiso de Residencia',
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 hole=0.3)  # Pie chart con un agujero en el centro (tipo donut)
    
    # Añadir texto de porcentajes y cantidades dentro del gráfico
    fig.update_traces(pull=pull_values)
    
    return fig


def graficar_combinaciones(dataframe):
    # Agrupación y conteo
    combinaciones = dataframe.groupby(['persona_racializada', 'persona_discapacitada', 'persona_sin_hogar', 'persona_migrante']).size().reset_index(name='Cantidad')
    
    # Crear una nueva columna que combine las condiciones
    combinaciones['Combinación'] = combinaciones.apply(
        lambda row: f"persona_racializada: {row['persona_racializada']}, persona_discapacitada: {row['persona_discapacitada']}, "
                    f"persona_sin_hogar: {row['persona_sin_hogar']}, persona_migrante: {row['persona_migrante']}", axis=1)
    
    # Configuración gráfico de barras
    fig = px.bar(combinaciones, 
                 x='Combinación', 
                 y='Cantidad', 
                 title='Frecuencia de Combinaciones de Condiciones',
                 labels={'Combinación': 'Combinación de Condiciones', 'Cantidad': 'Número de Personas'},
                 color='Cantidad',
                 color_continuous_scale='Viridis')

    # Etiquetas en el gráfico
    fig.update_layout(xaxis_tickangle=45)
    
    return fig


def buscar_ciudad(dataframe, ciudad_a_buscar):
    ciudad_filtrada = dataframe[dataframe['provincia'].str.lower() == ciudad_a_buscar.lower()]
    info_ciudad = {
        "Provincia": ciudad_a_buscar,
        "Cantidad": len(ciudad_filtrada)
        } if not ciudad_filtrada.empty else {
        "Provincia": ciudad_a_buscar,
        "Cantidad": 0
    }
    return info_ciudad


def obtener_top_5_ciudades(dataframe):
    ciudades_count = dataframe['provincia'].value_counts().reset_index()
    ciudades_count.columns = ['Provincia', 'Cantidad']
    top_5_ciudades = ciudades_count.head(5).to_dict(orient='records')
    return top_5_ciudades


def graficar_especialidad(dataframe):
    # Contar las frecuencias de los valores en la columna 'ambito laboral'
    especialidad_count = dataframe['ambito_laboral'].value_counts().reset_index()
    especialidad_count.columns = ['Ambito Laboral', 'Cantidad']
    
    # Calcular los porcentajes
    total = especialidad_count['Cantidad'].sum()
    especialidad_count['Porcentaje'] = (especialidad_count['Cantidad'] / total) * 100
    
    # Calcular el índice de la sección con el valor más grande
    max_value_index = especialidad_count['Cantidad'].idxmax()
    
    # Crear un vector donde la porción con el valor más grande será destacada
    pull_values = [0 if i != max_value_index else 0.1 for i in range(len(especialidad_count))]
    
    # Crear gráfico de pastel (pie chart) con cantidades y porcentajes
    fig = px.pie(
        especialidad_count,
        names='Ambito Laboral',
        values='Cantidad',
        title='Distribución de Especialidades',
        labels={'Ambito Laboral': 'Ambito Laboral'},
        color='Ambito Laboral',
        color_discrete_sequence=px.colors.qualitative.Set1,
        hole=0.3  # Tipo donut
    )
    
    # Añadir texto de porcentajes y cantidades dentro del gráfico
    fig.update_traces(pull=pull_values)
    
    return fig




#####Prueba
def prueba(dataframe, viven_espana=True):
    # Verificar que las columnas necesarias existen en el DataFrame
    columnas_requeridas = ['vives_en_espana', 'orientacion_sexual']
    for columna in columnas_requeridas:
        if columna not in dataframe.columns:
            raise ValueError(f"Falta la columna requerida: {columna}")

    # Filtrar el DataFrame según el parámetro
    filtro = dataframe['vives_en_espana'] == viven_espana
    df_filtrado = dataframe[filtro]
    
    # Conteo de orientaciones
    colectivos_count = df_filtrado['orientacion_sexual'].value_counts().reset_index()
    colectivos_count.columns = ['Orientacion', 'Cantidad']
    
    # Configurar título según el filtro
    titulo = "Distribución de Orientación Sexual"
    if viven_espana:
        titulo += " (Personas que Viven en España)"
    else:
        titulo += " (Personas que No Viven en España)"
    
    # Crear gráfico de pastel
    fig = px.pie(
        colectivos_count, 
        values='Cantidad', 
        names='Orientacion', 
        title=titulo,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    return fig