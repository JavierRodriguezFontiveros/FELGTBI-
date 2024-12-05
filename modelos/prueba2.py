from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, TextDataset, DataCollatorForLanguageModeling
from datasets import load_dataset
import pickle
import google.generativeai as genai
from dotenv import load_dotenv
import os
import google.generativeai as genai



api_key_gemini = os.getenv("GEMINI_API_KEY")

# try:
#     gemini_api_key = api_key_gemini
#     if not gemini_api_key:
#         raise ValueError("No utilices formato Markdown ni negrita, texto limpio. La variable GEMINI_API_KEY no está definida. Verifica tu archivo .env o las variables de entorno.")
#     genai.configure(api_key=gemini_api_key)
#     print("API configurada correctamente con la clave proporcionada.")
# except Exception as e:
#     print(f"Error al configurar la API: {e}")
#     raise

# def generar_respuesta(prompt):
#     try:
#         prompt_total = f"En contexto histórico LGTBI, responde: {prompt}"
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(prompt_total)
#         if not response or not hasattr(response, 'text'):
#             raise ValueError("Respuesta vacía o no válida del modelo.")
#         return response.text
#     except Exception as e:
#         return f"Error al generar respuesta para historia: {str(e)}"
    
# r = generar_respuesta("si puedo ir al cine seguro")
# print(r)









# 1. Cargar el modelo y el tokenizador preentrenado
# model_name = "gpt2"  # Puedes elegir cualquier otro modelo de Hugging Face
# model_name = "sentence-transformers/all-MiniLM-L6-v2"  # Puedes elegir cualquier otro modelo de Hugging Face
# model_name = "sentence-transformers/all-MiniLM-L6-v2"  # Puedes elegir cualquier otro modelo de Hugging Face
model = genai.GenerativeModel("gemini-1.5-flash")
# model = genai.GenerativeModel(model_name)

# Supongamos que tienes un archivo de texto plano 'data.txt'
def load_data(file_path):
    with open(file_path, encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return lines

data_file = "data.txt"  # Reemplaza esto con la ruta a tu archivo de datos
examples = load_data(data_file)

# Proceso de fine-tuning (la API de genai debería soportar algún método para el fine-tuning)
# NOTA: Ajusta esto basado en la documentación específica de genai
model.fine_tune(examples)

# Guardar el modelo afinado como pickle
with open('fine_tuned_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Modelo guardado como pickle.")

# Cargar el modelo desde el archivo pickle
with open('fine_tuned_model.pkl', 'rb') as f:
    model = pickle.load(f)

print("Modelo cargado desde pickle.")

# Función para generar texto a partir de un prompt
def generate_text(model, prompt):
    # Generar el texto con el modelo Gemini
    response = model.generate(prompt)
    return response

# Define tu prompt
prompt = "Eres un profesional sanitario experto en VIH. ¿Qué me puedes decir sobre la prevención?"

# Generar y mostrar el texto
generated_text = generate_text(model, prompt)
print("Texto generado:", generated_text)






prompt = "Eres un profesional sanitario experto en VIH. ¿Qué me puedes decir sobre la prevención?"
response = model.generate()
# model = AutoModelForCausalLM.from_pretrained(model_name)
# tokenizer = AutoTokenizer.from_pretrained(model_name)

# 2. Preparar los datos
# Suponiendo que tienes un archivo de texto plano 'data.txt'
def load_data(tokenizer, file_path, block_size=128):
    with open(file_path, encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    examples = tokenizer(lines, add_special_tokens=True, truncation=True, max_length=block_size)
    return examples

data_file = "data.txt"  # Reemplaza esto con la ruta a tu archivo de datos
examples = load_data(tokenizer, data_file)

# Crear el dataset
train_dataset = TextDataset(tokenizer=tokenizer, file_path=data_file, block_size=128)

# 3. Configurar los argumentos de entrenamiento
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    save_steps=10_000,
    save_total_limit=2,
)

# 4. Crear el collator de datos
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, 
    mlm=False,
)

# 5. Crear el entrenador
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
)

# 6. Afinar el modelo
trainer.train()


model = AutoModelForCausalLM.from_pretrained("./fine_tuned_model") 
tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_model")

# Guardar el modelo y el tokenizador como pickle 
with open('fine_tuned_model.pkl', 'wb') as f: 
    pickle.dump((model, tokenizer), f) 

print("Modelo y tokenizador guardados como pickle.")

# # 7. Guardar el modelo afinado
# model.save_pretrained("./fine_tuned_model")
# tokenizer.save_pretrained("./fine_tuned_model")

# print("Fine-tuning completado y modelo guardado.")


import pickle
from transformers import AutoModelForCausalLM, AutoTokenizer

# Cargar el modelo y el tokenizador desde el archivo pickle
with open('fine_tuned_model.pkl', 'rb') as f:
    model, tokenizer = pickle.load(f)

print("Modelo y tokenizador cargados desde pickle.")

# Función para generar texto a partir de un prompt
def generate_text(model, tokenizer, prompt, max_length=100):
    # Tokenizar el prompt
    inputs = tokenizer(prompt, return_tensors='pt')
    
    # Generar el texto
    output = model.generate(
        inputs['input_ids'], 
        max_length=max_length, 
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    
    # Decodificar y retornar el texto generado
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

# Define tu prompt
prompt = "Eres un profesional sanitario experto en VIH. ¿Qué me puedes decir sobre la prevención?"

# Generar y mostrar el texto
generated_text = generate_text(model, tokenizer, prompt)
print("Texto generado:", generated_text)
