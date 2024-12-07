from fastapi import FastAPI
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Cargar las variables de entorno
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Verificar que la clave esté configurada
if not gemini_api_key:
    raise EnvironmentError("La variable GEMINI_API_KEY no está configurada. Verifica el archivo .env.")

# Configurar el modelo generativo
genai.configure(api_key=gemini_api_key)

# Crear la aplicación FastAPI
app = FastAPI()

@app.get("/test_model/")
async def test_model(prompt: str):
    try:
        # Llamar al modelo con el prompt proporcionado
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        # Verificar y devolver la respuesta
        if not response or not hasattr(response, 'text'):
            return {"error": "Respuesta vacía o no válida del modelo."}

        return {"respuesta": response.text}

    except Exception as e:
        return {"error": str(e)}

# Instrucciones para ejecutar este script
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
