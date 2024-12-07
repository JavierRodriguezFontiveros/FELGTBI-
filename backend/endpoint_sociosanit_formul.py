

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
from enum import Enum

class Province(str, Enum):
    alava = "Álava"
    albacete = "Albacete"
    alicante = "Alicante"
    almeria = "Almería"
    avila = "Ávila"
    badajoz = "Badajoz"
    barcelona = "Barcelona"
    burgos = "Burgos"
    caceres = "Cáceres"
    cadiz = "Cádiz"
    cantabria = "Cantabria"
    castellon = "Castellón"
    ceuta = "Ceuta"
    cordoba = "Córdoba"
    cuenca = "Cuenca"
    girona = "Girona"
    granada = "Granada"
    guadalajara = "Guadalajara"
    girona = "Girona"
    huelva = "Huelva"
    huesca = "Huesca"
    jaen = "Jaén"
    la_rioja = "La Rioja"
    las_palmas = "Las Palmas"
    leon = "León"
    lugo = "Lugo"
    madrid = "Madrid"
    malaga = "Málaga"
    melilla = "Melilla"
    murcia = "Murcia"
    navarra = "Navarra"
    ourense = "Ourense"
    palencia = "Palencia"
    pontevedra = "Pontevedra"
    salamanca = "Salamanca"
    segovia = "Segovia"
    sevilla = "Sevilla"
    soria = "Soria"
    tarragona = "Tarragona"
    teruel = "Teruel"
    toledo = "Toledo"
    valencia = "Valencia"
    valladolid = "Valladolid"
    vizcaya = "Vizcaya"
    zamora = "Zamora"
    zaragoza = "Zaragoza"
    fuera_espana = "Fuera de España"

class WorkEnvironment(str, Enum):
    centro_salud = "Centro de Salud"
    hospital = "Hospital"
    centro_comunitario = "Centro comunitario"
    consulta_privada = "Consulta privada"
    asociacion = "Asociación"
    otro = "Otro"

#Clase Completa
class SociosanitaryData(BaseModel):
    provincia: Province
    ambito_laboral: WorkEnvironment

@app.post("/submit-data")
async def submit_data(sociosanitary_data: SociosanitaryData):
    connection = connect_to_db()
    if connection is None:
        raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos")
    
    cursor = connection.cursor()

    # Aquí ajustamos la consulta y los datos
    query = """
           INSERT INTO sociosanitarios_formulario (provincia, 
                                                    ambito_laboral)
           VALUES (%(provincia)s, %(ambito_laboral)s)
    """
    
    data = {
            "provincia": sociosanitary_data.provincia,
            "ambito_laboral": sociosanitary_data.ambito_laboral
            }

    try:
        cursor.execute(query, data)
        connection.commit()
        return {"message": "Datos enviados y almacenados correctamente"}
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        connection.rollback()
        raise HTTPException(status_code=500, detail="Error al guardar los datos")
    finally:
        cursor.close()
        connection.close()



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''