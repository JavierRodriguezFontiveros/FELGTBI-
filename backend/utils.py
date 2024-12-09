#Bibliotecas:
import psycopg2
import os
from dotenv import load_dotenv
import pandas as pd

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#Conexión base de datos:
def connect_to_db():
    
    load_dotenv(dotenv_path="../credenciales.env")
    
    #Acceder a las variables de entorno
    db_host = os.getenv("DB_HOST_AWS")
    db_username = os.getenv("DB_USER_AWS")
    db_password = os.getenv("DB_PASSWORD_AWS")
    db_database = os.getenv("DB_DATABASE_AWS")
    db_port = int(os.getenv("DB_PORT_AWS", 5432))


    # print(f"DB Host: {db_host}")
    # print(f"DB User: {db_username}")
    # print(f"DB Password: {db_password}")
    # print(f"DB Database: {db_database}")
    # print(f"DB Port: {db_port}")

    #Probando la conexión:
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
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def fetch_all_from_table(table_name: str) -> dict:
    valid_tables = {"categorias_chatbot", "preguntas_chatbot", "opciones_chatbot"}
    if table_name not in valid_tables:
        raise ValueError("Invalid table name provided.")

    conn = connect_to_db()
    if not conn:
        raise RuntimeError("Database connection could not be established.")

    try:
        with conn.cursor() as cur:
            query = f"SELECT * FROM {table_name};"
            cur.execute(query)
            rows = cur.fetchall()
            column_names = [desc[0] for desc in cur.description]
            return [dict(zip(column_names, row)) for row in rows]
    
    except Exception as e:
        raise RuntimeError(f"Error fetching data: {e}")
    finally:
        conn.close()
    

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def modify_table_records(table_name:str, column:str, new_value:str, id:int) -> None:
    valid_tables = {"categorias_chatbot", "preguntas_chatbot", "opciones_chatbot"}
    
    if table_name not in valid_tables:
        raise ValueError("Invalid table name provided.")
    
    conn = connect_to_db()
    if not conn:
        raise RuntimeError("Database connection could not be established.")

    try:
        with conn.cursor() as cur:
            query = f"UPDATE {table_name} SET {column} = {new_value} WHERE id = {id};"
            cur.execute(query)
    
    except Exception as e:
        raise RuntimeError(f"Error fetching data: {e}")
    finally:
        conn.close()

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
prompt_basico = (
    "Eres un experto sociosanitario especializado en vih y sida. Pero no digas que lo eres, actúa como tal."
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
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#Gráficos:
import plotly.io as pio
import plotly.express as px


#Configurar los renderer
pio.renderers.default = "svg"

def grafico_pie(dataframe, viven_espana=True):
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
    fig = px.pie(colectivos_count, 
                 values='Cantidad', 
                 names='Orientacion', 
                 title=titulo,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    
    return fig

def create_bar_chart_plotly_html(df):

    try:
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

        # Crear el gráfico de barras con Plotly
        fig = px.bar(
            edad_grupo,
            x='grupo_edad',
            y='cantidad',
            title="Distribución de Edad por Grupo",
            labels={'grupo_edad': "Grupo de Edad", 'cantidad': "Cantidad de Personas"},
            text='cantidad'
        )

        # Ajustar diseño del gráfico
        fig.update_traces(marker_color='blue', textposition='outside')
        fig.update_layout(xaxis_title="Grupo de Edad", yaxis_title="Cantidad de Personas")

        # Exportar el gráfico como HTML
        return fig.to_html(full_html=False)
    except Exception as e:
        raise RuntimeError(f"Error al generar el gráfico: {e}")
    



def barras_apiladas_genero_orientacion_html(dataframe):

    try:
        # Agrupar y contar las combinaciones de género y orientación
        datos_agrupados = dataframe.groupby(['identidad_genero', 'orientacion_sexual']).size().reset_index(name='Cantidad')

        # Configurar el gráfico de barras apiladas
        fig = px.bar(
            datos_agrupados,
            x='identidad_genero',
            y='Cantidad',
            color='orientacion_sexual',
            title='Distribución de Género y Orientación Sexual',
            labels={'identidad_genero': 'Género', 'orientacion_sexual': 'Orientación Sexual'},
            barmode='stack',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        # Exportar el gráfico como HTML
        return fig.to_html(full_html=False)
    except Exception as e:
        raise RuntimeError(f"Error al generar el gráfico: {e}")





def graficar_permiso_residencia_html(dataframe):
    """
    Genera un gráfico de pastel (pie chart) sobre la distribución de permisos de residencia,
    basado en un DataFrame dado, y lo devuelve como HTML.

    Args:
        dataframe (pd.DataFrame): DataFrame con la columna 'permiso_residencia'.

    Returns:
        str: El contenido HTML del gráfico generado.
    """
    try:
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
        fig = px.pie(
            permiso_count,
            names='Permiso de Residencia',
            values='Cantidad',
            title='Distribución de Permisos de Residencia',
            labels={'Permiso de Residencia': 'Tipo de Permiso'},
            color='Permiso de Residencia',
            color_discrete_sequence=px.colors.qualitative.Set1,
            hole=0.3  # Pie chart con un agujero en el centro (tipo donut)
        )

        # Añadir texto de porcentajes y cantidades dentro del gráfico
        fig.update_traces(pull=pull_values)

        # Exportar el gráfico como HTML
        return fig.to_html(full_html=False)
    except Exception as e:
        raise RuntimeError(f"Error al generar el gráfico: {e}")
    
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


def graficar_especialidad_html(dataframe):
    """
    Genera un gráfico de pastel (pie chart) sobre la distribución de especialidades,
    basado en un DataFrame dado, y lo devuelve como HTML.

    Args:
        dataframe (pd.DataFrame): DataFrame con la columna 'ambito_laboral'.

    Returns:
        str: El contenido HTML del gráfico generado.
    """
    try:
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

        # Exportar el gráfico como HTML
        return fig.to_html(full_html=False)
    except Exception as e:
        raise RuntimeError(f"Error al generar el gráfico: {e}")




#Funciona
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
    fig = px.pie(colectivos_count, 
                 values='Cantidad', 
                 names='Orientacion', 
                 title=titulo,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    
    return fig