from dotenv import load_dotenv
import os
import re
from langchain_community.tools import GooglePlacesTool

#Warnings
import warnings
warnings.filterwarnings("ignore")


# Cargar las variables de entorno desde el archivo .env
load_dotenv(dotenv_path="../credenciales.env")

# Configuración de la API de Google Places
google_places = os.getenv("GPLACES_API_KEY")
os.environ["GPLACES_API_KEY"] = google_places

# Crear instancia de GooglePlacesTool
places = GooglePlacesTool()


try:
    prompt_maps = f"Centros vih " + provincia
    respuesta_google_maps = places.run(prompt_maps)
    pattern = re.compile(r"(\d+)\.\s*(.*?)\nAddress:\s*(.*?)\nGoogle place ID:\s*(.*?)\nPhone:\s*(.*?)\nWebsite:\s*(.*?)\n", re.DOTALL)
    matches = pattern.findall(respuesta_google_maps)

    matches = list({match[0]: match for match in matches}.values())

    matches = matches[:3]  # Muestra solo los primeros 3 resultados

    locations_str = ""
    for match in matches:
        location_info = (
            f"ID: {int(match[0])}\n"
            f"Name: {match[1].strip()}\n"
            f"Address: {match[2].strip()}\n"
            f"Phone: {match[4].strip() if match[4].strip() != 'Unknown' else 'N/A'}\n"
            f"Website: {match[5].strip() if match[5].strip() != 'Unknown' else 'N/A'}\n"
            f"{'-' * 40}\n"  # Separador entre cada ubicación
        )
        locations_str += location_info

    # Imprimir el resultado en consola
    print(locations_str)
    print(provincia)


except Exception as e:
    print(f"Hubo un error al realizar la búsqueda: {e}")