from dotenv import load_dotenv
import os
from langchain_community.tools import GooglePlacesTool
import re

#Configuracion de la API google Places:
load_dotenv(dotenv_path="../credenciales.env")
google_places = os.getenv("GPLACES_API_KEY")
os.environ["GPLACES_API_KEY"] = google_places
# Crear instancia de GooglePlacesTool
places = GooglePlacesTool()
# Realizar la búsqueda
try:
    prompt_maps = "Centros vih en Sevilla " 
    respuesta_google_maps = places.run(prompt_maps)
    pattern = re.compile(r"(\d+)\.\s*(.*?)\nAddress:\s*(.*?)\nGoogle place ID:\s*(.*?)\nPhone:\s*(.*?)\nWebsite:\s*(.*?)\n",re.DOTALL)
    matches = pattern.findall(respuesta_google_maps)
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

    print(locations_str)
except Exception as e:
    print(f"Hubo un error al realizar la búsqueda: {e}")