from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
import os

# Crear la app FastAPI
app = FastAPI()

# Configuración de plantillas
templates = Jinja2Templates(directory="templates")

# Leer el JSON
JSON_PATH = os.path.join("JSONs", "sociosanitario.json")

def cargar_json():
    with open(JSON_PATH, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

# Ruta para devolver el JSON completo
@app.post("/sociosanitario/")
async def devolver_json():
    datos = cargar_json()
    return JSONResponse(datos)

# Ruta para renderizar la página inicial
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    datos = cargar_json()
    opciones = [datos[clave]["profesional"] for clave in datos]
    return templates.TemplateResponse("index.html", {"request": request, "opciones": opciones})

# Ruta para devolver las subopciones según el profesional
@app.post("/necesidades/")
async def obtener_necesidades(data: dict):
    profesional_seleccionado = data.get("profesional")
    datos = cargar_json()
    for clave, contenido in datos.items():
        if contenido["profesional"] == profesional_seleccionado:
            return JSONResponse({"necesidades": contenido["necesidades"]})
    return JSONResponse({"error": "Profesional no encontrado"}, status_code=404)
