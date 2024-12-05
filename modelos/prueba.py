from huggingface_hub import InferenceClient
from langchain import PromptTemplate
import os
from langchain.document_loaders import PyPDFLoader
# from langchain_core.prompts import ChatPromptTemplate

from transformers import AutoModel, AutoTokenizer
import torch

from langchain.chains import create_retrieval_chain

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI



model = "microsoft/Phi-3.5-mini-instruct"  

# retriever = ...  # Your retriever
# llm = 

# system_prompt = (
#     "Use the given context to answer the question. "
#     "If you don't know the answer, say you don't know. "
#     "Use three sentence maximum and keep the answer concise. "
#     "Context: {context}"
# )
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         ("human", "{input}"),
#     ]
# )
# question_answer_chain = create_stuff_documents_chain(llm, prompt)
# chain = create_retrieval_chain(retriever, question_answer_chain)

# chain.invoke({"input": query})



# # Load docs
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import FAISS
# from langchain_openai.chat_models import ChatOpenAI
# from langchain_openai.embeddings import OpenAIEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
# data = loader.load()

# # Split
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
# all_splits = text_splitter.split_documents(data)

# # Store splits
# vectorstore = FAISS.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

# # LLM
# llm = ChatOpenAI()



# qa_chain = RetrievalQA(llm=llm, retriever=vectorstore.as_retriever())
# response = qa_chain.run(query)
# print(response)

# Función para obtener embeddings usando Hugging Face
def get_embeddings(sentence, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    
    inputs = tokenizer(sentence, return_tensors="pt")
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    
    return embeddings




from langchain.document_loaders import PyPDFLoader


from langchain.text_splitter import CharacterTextSplitter


from langchain.embeddings import OpenAIEmbeddings 
from langchain.vectorstores import FAISS 



# loader = PyPDFLoader('./documento_informativo_sobre_infeccion_vih_profesionales.pdf')
# data = loader.load()
# data

# [Document(page_content='Harry Potter and the Methods of Rationality', metadata={'source': '../datasets/harry_potter_pdf/hpmor-trade-classic.pdf', 'page': 0}),
# Document(page_content='', metadata={'source': '../datasets/harry_potter_pdf/hpmor-trade-classic.pdf', 'page': 1}), ...


opc_diagnostico= "Si"

if opc_diagnostico.lower() == "si":
    output_diagnostico = "y sí estoy diagnosticado"
elif opc_diagnostico.lower() == "no":
    output_diagnostico = "y no estoy diagnosticado"
elif opc_diagnostico.lower() == "No sé":
    output_diagnostico = ""

opc_pronombre = "Elle"

if opc_pronombre.lower() == "el":
    output_pronombre = "El"
elif opc_pronombre.lower() == "ella":
    output_pronombre = "Ella"
elif opc_pronombre.lower() == "elle":
    output_pronombre = "Elle"
    
    
fecha_diagnostico = "17/03/2010"

# Definir el contenido del prompt
template = """Eres un profesional sanitario experto en vih. 
            Y mi situación es que tengo vih diagnosticado desde {fecha_diagnostico} {output_diagnostico}. 
            Dame la respuesta hablandome con el pronombre {output_pronombre}. 
            Y que sea una respuesta muy corta."""


# # Crear el prompt template
prompt = PromptTemplate(input_variables=["output_pronombre","fecha_diagnostico","output_diagnostico"], template=template)

# Función para formatear el prompt
def format_prompt(output_pronombre,fecha_diagnostico,output_diagnostico):
    return prompt.format(output_pronombre=output_pronombre,fecha_diagnostico=fecha_diagnostico,output_diagnostico=output_diagnostico)

# def format_prompt(sentence, prompt_template): 
#     return prompt_template.format(sentence=sentence)

# Función para obtener la respuesta del modelo
def get_model_response(api_key, model, formatted_prompt):
    client = InferenceClient(api_key=api_key)
    
    messages = [
        {
            "role": "user",
            "content": formatted_prompt
        }
    ]
    
    completion = client.chat.completions.create(
        model=model, 
        messages=messages, 
        max_tokens=500
    )
    
    return completion.choices[0].message.content




# Formatear el prompt
formatted_prompt = format_prompt(output_pronombre,fecha_diagnostico,output_diagnostico)

# Obtener la respuesta del modelo
response = get_model_response(api_key, model, formatted_prompt)




loader = PyPDFLoader("documento_informativo_sobre_infeccion_vih_profesionales.pdf")
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)


embeddings = get_embeddings(formatted_prompt,model)

vectorstore = FAISS.from_documents(docs, embeddings)

# Mostrar la respuesta
print(response)
print("holi")



