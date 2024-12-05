# Bibliotecas:
from fastapi import FastAPI #Api
import uvicorn #Despliegue en Local

from fastapi.responses import StreamingResponse
import io
import matplotlib.pyplot as plt

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
app = FastAPI()



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/")
async def home():
    return {"message": """
Hola buenas bienvenido a este proyecto de tripulaciones
                   """}




''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
@app.get("/bar-chart/")
def generate_bar_chart():
    # Datos de ejemplo
    categories = ["A", "B", "C", "D"]
    values = [10, 20, 15, 5]

    # Crear el gráfico de barras
    plt.figure(figsize=(8, 6))
    plt.bar(categories, values, color="blue", alpha=0.7)
    plt.title("Gráfico de Barras")
    plt.xlabel("Categorías")
    plt.ylabel("Valores")

    # Guardar el gráfico en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # Devolver el gráfico como una respuesta
    return StreamingResponse(buf, media_type="image/png")





''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Punto de entrada principal
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)