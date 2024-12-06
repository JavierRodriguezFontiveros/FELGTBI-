import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

responses = {}  # Guardar respuestas acumuladas

def get_response_from_gemini(prompt):
    # Simula diferentes respuestas basadas en el flujo
    if "Dame una receta de estilo de cocina" in prompt:
        style = prompt.split("cocina ")[-1]
        return f"Aquí tienes una receta de {style}: ... [receta simulada]"
    elif prompt == "1":
        return "Selecciona el estilo de comida: 1. Americana, 2. Italiana, 3. Asiática"
    elif prompt in ["Americana", "Italiana", "Asiática"]:
        return f"Dame una receta de estilo de cocina {prompt}"
    else:
        return "Lo siento, no entendí eso."

def chatbot():
    print("¡Bienvenido al chatbot interactivo!")
    print("Selecciona una opción: 1. Tipo de comida, 2. Tipo de película")

    choice = input("Elige una opción: ")

    if choice == "1":
        print(get_response_from_gemini("1"))
        style = input("Selecciona un estilo: Americana, Italiana, Asiática: ")
        responses["style"] = style
        print(get_response_from_gemini(style))
    else:
        print("Opción no implementada. Por favor selecciona 1.")

if __name__ == "__main__":
    chatbot()
