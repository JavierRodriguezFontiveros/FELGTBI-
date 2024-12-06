from fastapi import FastAPI
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

@app.post("/api/chat")
async def process_chat(data: dict):
    prompt = data.get("prompt", "")
    if not prompt:
        return JSONResponse(content={"response": "Prompt vacío"}, status_code=400)
    
    response = get_response_from_gemini(prompt)
    return JSONResponse(content={"response": response})
