from fastapi import FastAPI
import json
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

# Configuración de plantillas
templates = Jinja2Templates(directory="templates")

# Simulación de respuestas dinámicas
simulated_responses = {
    "1": "Selecciona el estilo de comida: Americana, Italiana, Asiática",
    "Americana": "Dame una receta de estilo de cocina Americana",
    "Italiana": "Dame una receta de estilo de cocina Italiana",
    "Asiática": "Dame una receta de estilo de cocina Asiática",
}

def get_response_from_gemini(prompt):
    # Lógica simulada
    if "Dame una receta de estilo de cocina" in prompt:
        style = prompt.split("cocina ")[-1]
        return f"Aquí tienes una receta de {style}: ... [receta simulada]"
    return simulated_responses.get(prompt, "Lo siento, no entendí eso.")

@app.get("/", response_class=HTMLResponse)
async def serve_html():
    return templates.TemplateResponse("chatbot.html", {"request": {}})

@app.post("/sociosanitario/")
async def devolverJSON(data: dict):
    with open('/JSONs/sociosanitario.json', 'r') as archivo:
        datos = json.load(archivo)
    return JSONResponse(datos)
