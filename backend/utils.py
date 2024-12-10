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
def check_admin_details(email: str, password: str) -> bool:
    conn = connect_to_db()  
    if not conn:
        raise RuntimeError("Database connection could not be established.")
    
    try:
        with conn.cursor() as cur:
            query = "SELECT * FROM admin_data WHERE email = %s AND password = %s;"
            cur.execute(query, (email, password))
            result = cur.fetchone()
            if result:
                return True  # Valid credentials
            else:
                return False  # Invalid credentials
        
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


###EDITADA###
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
    
    # Calcular los porcentajes
    total = colectivos_count['Cantidad'].sum()
    colectivos_count['Porcentaje'] = (colectivos_count['Cantidad'] / total) * 100
    
    # Redondear los porcentajes a enteros
    colectivos_count['Porcentaje_Redondeado'] = colectivos_count['Porcentaje'].round().astype(int)

    # Ajustar los residuos para asegurar que la suma de los porcentajes es 100
    diferencia = 100 - colectivos_count['Porcentaje_Redondeado'].sum()
    if diferencia > 0:
        # Ajustar los porcentajes más grandes para cerrar la diferencia
        ajuste_indices = colectivos_count.nlargest(diferencia, 'Porcentaje').index
        colectivos_count.loc[ajuste_indices, 'Porcentaje_Redondeado'] += 1

    # Configurar título según el filtro
    titulo = "Distribución de Orientación Sexual"
    if viven_espana:
        titulo += " (Personas que Viven en España)"
    else:
        titulo += " (Personas que No Viven en España)"
    
    # Crear gráfico de pastel
    fig = px.pie(colectivos_count, 
                 values='Porcentaje_Redondeado', 
                 names='Orientacion', 
                 title=titulo,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    
    # Personalizar el gráfico
    fig.update_traces(
        textinfo='percent',  # Mostrar solo el porcentaje dentro del gráfico
        textfont_size=14,  # Ajustar el tamaño del texto
        pull=[0.1 if i == colectivos_count['Porcentaje_Redondeado'].idxmax() else 0 for i in range(len(colectivos_count))]  # Resaltar la sección más grande
    )

    # Ajustar el diseño del gráfico con el título y formato adicional
    fig.update_layout(
        title={'text': "Distribución de Orientación Sexual<br><span style='font-size:14px;color:gray;'>El gráfico muestra los porcentajes por cada orientación sexual.</span>",
               'x': 0.5, 
               'xanchor': 'center'},  # Centrado del título
        title_font=dict(size=22),
        xaxis_title_font=dict(size=18),  
        yaxis_title_font=dict(size=18),  
        xaxis_tickfont=dict(size=16),  
        yaxis_tickfont=dict(size=16),  
        showlegend=True,  # Mostrar la leyenda
        legend_title="Orientación Sexual",  # Título de la leyenda
        legend=dict(
            x=1,  # Mover la leyenda a la derecha del gráfico
            xanchor='left',  # Alineación de la leyenda a la izquierda
            y=0.5,  # Alineación vertical de la leyenda
            yanchor='middle',  # Centrar la leyenda en el medio
            traceorder='normal',  # Orden de las leyendas
            font=dict(size=14),  # Tamaño de la fuente en la leyenda
            bgcolor="white",  # Fondo blanco para la leyenda
            bordercolor="Black",  # Borde de la leyenda
            borderwidth=1  # Grosor del borde de la leyenda
        ),
        plot_bgcolor="white",  # Fondo blanco para el área del gráfico
        paper_bgcolor="white",  # Fondo blanco para el gráfico completo
    )

    return fig



###EDITADA###
def create_bar_chart_plotly_html(df):
    try:
        # Definir los rangos de edades y las etiquetas correspondientes
        bins = [0, 15, 19, 24, 29, 39, 49, 59, 100]
        labels = ['Menores de 16', '15-19', '20-24', 
                  '25-29', '30-39', 
                  '40-49', '50-59', 'Mayores de 60']

        # Asegurarse de que la columna 'edad' está en formato numérico
        df['edad'] = pd.to_numeric(df['edad'], errors='coerce')

        # Crear una nueva columna 'grupo_edad' con las categorías de edad
        df['grupo_edad'] = pd.cut(df['edad'], bins=bins, labels=labels, right=False)

        # Calcular la cantidad de personas en cada grupo de edad
        edad_grupo = df.groupby('grupo_edad').size().reset_index(name='cantidad')

        # Calcular el porcentaje sobre el total
        total = edad_grupo['cantidad'].sum()
        edad_grupo['porcentaje'] = (edad_grupo['cantidad'] / total * 100)

        # Aplicar redondeo sin exceder el 100%
        edad_grupo['porcentaje_entero'] = edad_grupo['porcentaje'].apply(int)  # Parte entera
        edad_grupo['residuo'] = edad_grupo['porcentaje'] - edad_grupo['porcentaje_entero']
        diferencia = 100 - edad_grupo['porcentaje_entero'].sum()

        # Ajustar los residuos más altos para cerrar la diferencia
        if diferencia > 0:
            ajuste_indices = edad_grupo.nlargest(diferencia, 'residuo').index
            edad_grupo.loc[ajuste_indices, 'porcentaje_entero'] += 1

        # Crear el gráfico de barras con un solo color
        fig = px.bar(
            edad_grupo,
            x='grupo_edad',
            y='porcentaje_entero',
            title="Distribución de Edad",
            labels={'grupo_edad': "Grupo de Edad", 'porcentaje_entero': "Porcentaje (%)"},
            text='porcentaje_entero',
            color_discrete_sequence=["#F1A7C2"])

        
        fig.update_traces(textposition='outside')  

        # Eliminar la leyenda y centrar el título
        fig.update_layout(xaxis_title="Grupo de Edad", 
                          yaxis_title="Porcentaje (%)",
                          xaxis=dict(tickangle=0),
                          plot_bgcolor="white",  
                          paper_bgcolor="white",  
                          showlegend=False,  
                          title={'text': "Distribución de edades por grupo<br><span style='font-size:14px;color:gray;'>El gráfico muestra los porcentajes por grupo de edad.</span>",
                                 'x': 0.5,
                                 'xanchor': 'center'},
                          title_font=dict(size=22),
                          xaxis_title_font=dict(size=18),  
                          yaxis_title_font=dict(size=18),  
                          xaxis_tickfont=dict(size=16),  
                          yaxis_tickfont=dict(size=16))

        # Exportar el gráfico como HTML
        return fig.to_html(full_html=False)
    except Exception as e:
        raise RuntimeError(f"Error al generar el gráfico: {e}")








###EDITADA###

def barras_apiladas_genero_orientacion_html(dataframe):

    try:
        # Agrupar y contar las combinaciones de género y orientación
        datos_agrupados = dataframe.groupby(['identidad_genero', 'orientacion_sexual']).size().reset_index(name='Cantidad')

        # Normalizar dentro de cada grupo de género
        datos_agrupados['Proporcion'] = datos_agrupados.groupby('identidad_genero')['Cantidad'].transform(lambda x: x / x.sum())

        # Configurar el gráfico de barras apiladas
        fig = px.bar(
            datos_agrupados,
            x='identidad_genero',
            y='Proporcion',
            color='orientacion_sexual',
            title='Distribución de identidades de género y orientaciones sexuales',
            labels={'Proporcion': 'Proporción', 'identidad_genero': 'Identidad de Género', 'orientacion_sexual': 'Orientación Sexual'},
            barmode='stack',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        # Añadir subtítulo al gráfico
        fig.update_layout(
            title={
                'text': "Distribución de identidades de género y orientaciones sexuales<br><span style='font-size:18px;color:gray;'>El gráfico muestra la proporción de orientaciones sexuales dentro de cada identidad de género.</span>",
                'x': 0.5,  # Centrado horizontalmente
                'xanchor': 'center'},
            plot_bgcolor='white',
            paper_bgcolor='white',
            title_font=dict(size=22),
            xaxis_title_font=dict(size=18),  
            yaxis_title_font=dict(size=18),  
            xaxis_tickfont=dict(size=16),  
            yaxis_tickfont=dict(size=16),
            legend_font=dict(size=14)
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
        fig = px.pie(permiso_count,
                    names='Permiso de Residencia',
                    values='Cantidad',
                    title='Distribución de Permisos de Residencia',
                    labels={'Permiso de Residencia': 'Tipo de Permiso'},
                    color='Permiso de Residencia',
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    hole=0.3) 

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


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def obtener_top_5_ciudades(dataframe):

    ciudades_count = dataframe['provincia'].value_counts().reset_index()
    ciudades_count.columns = ['Provincia', 'Cantidad']
    top_5_ciudades = ciudades_count.head(5).to_dict(orient='records')
    return top_5_ciudades


def graficar_top_5_ciudades(dataframe):
    # Obtener las 5 ciudades más frecuentes
    top_5_ciudades = obtener_top_5_ciudades(dataframe)
    
    # Ordenar las ciudades de mayor a menor según la cantidad
    top_5_ciudades = sorted(top_5_ciudades, key=lambda x: x['Cantidad'], reverse=True)

    # Crear gráfico de barras con Plotly
    fig = px.bar(top_5_ciudades, 
                 x='Provincia', 
                 y='Cantidad', 
                 title="Top 5 Ciudades Más Frecuentes",
                 labels={'Provincia': 'Ciudad', 'Cantidad': 'Frecuencia'},
                 color='Provincia',
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    
    # Personalizar el gráfico
    fig.update_layout(
        title={'text': "Top 5 Ciudades Más Frecuentes<br><span style='font-size:14px;color:gray;'>Las cinco ciudades más frecuentes en los datos.</span>",
               'x': 0.5, 
               'xanchor': 'center'},
        title_font=dict(size=22),
        xaxis_title_font=dict(size=18),  
        yaxis_title_font=dict(size=18),  
        xaxis_tickfont=dict(size=16),  
        yaxis_tickfont=dict(size=16),  
        plot_bgcolor="white",  # Fondo blanco para el área del gráfico
        paper_bgcolor="white",  # Fondo blanco para el gráfico completo
    )
    
    return fig





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
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.3  # Tipo donut
        )

        # Añadir texto de porcentajes y cantidades dentro del gráfico
        fig.update_traces(pull=pull_values)

        # Exportar el gráfico como HTML
        return fig.to_html(full_html=False)
    except Exception as e:
        raise RuntimeError(f"Error al generar el gráfico: {e}")



