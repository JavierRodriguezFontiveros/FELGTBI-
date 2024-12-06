# EJEMPLO DE JSON RECIBIDO:
# {
#     "1.1": {
#       "titulo": "Tengo VIH",
#       "preguntas": {
#         "¿Cuándo te diagnosticaron?": [
#           "Hace menos de 6 meses" 
#         ],
#         "¿Estás en tratamiento TAR?": [
#           "Sí"
#         ],
#         "¿Tienes acceso a un médico?": [
#           "Sí"
#         ],
#         "¿Quieres información sobre algún tema?": [

#           "Apoyo psicológico"
#         ]
#       }
#     }

provincia = "Asturias"
pronombres= "Elle"

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import google.generativeai as genai
app = FastAPI()

# Definir el esquema para la solicitud entrante
class UserData(BaseModel):
    data: Dict[str, Any]

def generar_respuesta(prompt):
    try:
        prompt_total = f"En contexto histórico LGTBI, responde: {prompt}"
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt_total)
        if not response or not hasattr(response, 'text'):
            raise ValueError("Respuesta vacía o no válida del modelo.")
        return response.text
    except Exception as e:
        return f"Error al generar respuesta para historia: {str(e)}"
@app.post("/personalizar_prompt")
async def personalizar_prompt(user_data: UserData):
    try:
        # Determinar el tipo de sección y construir el prompt dinámicamente
        for key, seccion in user_data.data.items():
            titulo = seccion.get("titulo", "No especificado")
            preguntas = seccion.get("preguntas", {})

            # Verificar el tipo de sección
            if key.startswith("1.1"):
                tiempo_diagnostico = preguntas.get("¿Cuándo te diagnosticaron?", ["No especificado"])[0]
                en_tratamiento = preguntas.get("¿Estás en tratamiento TAR?", ["No especificado"])[0]
                acceso_medico = preguntas.get("¿Tienes acceso a un médico?", ["No especificado"])[0]
                informacion_necesaria = preguntas.get("¿Quieres información sobre algún tema?", ["Ninguna"])[0]

                # Crear el prompt para la sección 1.1
                prompt = ("Eres un especialista sociosanitario en VIH, hablas con compasión y tacto. Mis prnombres son:" + pronombres + "Vivo en" +provincia+ "Tengo VIH diagnosticado desde " + tiempo_diagnostico + "¿Qué si estoy en tratamiento?" + en_tratamiento + ". Y además " + acceso_medico + "tengo acceso médico. La información que solicito es:"+ informacion_necesaria + "."
                )

            elif key.startswith("1.2"):
                tipo_exposicion = preguntas.get("¿Qué tipo de exposición fue?", ["No especificado"])[0]
                tiempo_exposicion = preguntas.get("¿Cuándo ocurrió la posible infección?", ["No especificado"])[0]
                acceso_medico = preguntas.get("¿Tienes acceso a un médico?", ["No especificado"])[0]
                conocimiento_pep = preguntas.get("¿Sabes qué es la PEP?", ["No especificado"])[0]

                # Crear el prompt para la sección 1.2
                prompt = (
                    "Título: " + titulo + ". \n"
                    "Tipo de exposición: " + tipo_exposicion + ". \n"
                    "Tiempo desde la exposición: " + tiempo_exposicion + ". \n"
                    "Acceso a médico: " + acceso_medico + ". \n"
                    "Conocimiento sobre PEP: " + conocimiento_pep + "."
                )

            elif key.startswith("1.3"):
                tema_informacion = preguntas.get("¿Sobre qué tema quieres información?", ["No especificado"])[0]

                # Crear el prompt para la sección 1.3
                prompt = (
                    "Título: " + titulo + ". \n"
                    "Tema de interés: " + tema_informacion + "."
                )

            else:
                prompt = "Título: " + titulo + ". No se encontró un formato específico para esta sección."

            # Generar la respuesta del modelo
            respuesta_chatbot = generar_respuesta(prompt)

            # Devolver la respuesta del chatbot
            return {"respuesta_chatbot": respuesta_chatbot}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))