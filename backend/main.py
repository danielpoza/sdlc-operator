# /app/backend/main.py
import time

from fastapi import FastAPI
import urllib.parse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain import PromptTemplate, LLMChain
from contextlib import asynccontextmanager
from bs4 import BeautifulSoup
from typing import List


    
# Importa el módulo o la clase de LangChain que necesites.
# Aquí usamos OpenAI como ejemplo.
from langchain_community.llms import OpenAI
from ollama import chat
from pydantic import BaseModel
from atlassian import Confluence  
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser

import os

#Clase que define la estructura de respuesta del LLM
class Instruction(BaseModel):
    title: str
    root: str
    content: str  # Aquí se espera código HTML

class ChatResponse(BaseModel):
    user: str            # Texto para el chat
    process: List[Instruction]  # Lista de instrucciones

#Parser de Langchain para forzar que la respuesta cumpla el formato definido
output_parser = PydanticOutputParser(pydantic_object=ChatResponse)


load_dotenv()
summary_template = ""

#Función que se ejecutará al inicializar el servidor: 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: código que se ejecuta al iniciar la aplicación
    print("INICIO SERVICIO BACKEND SDLC OPERATOR")
    #Lectura contexto Confluence
    initcommand = get_confluence_page("CS", urllib.parse.unquote_plus("Inicialización"))
    content = get_confluence_page("CS", urllib.parse.unquote_plus("ArquitecturaServicios"))
    content2 = get_confluence_page("CS", urllib.parse.unquote_plus("Normativa"))
    content_po = get_confluence_page("CS", urllib.parse.unquote_plus("Instrucciones+para+definir+a+alto+nivel+un+servicio"))
    app.state.confluence_page = content
    #Iniciación del LLM
    instrucciones = "Instrucciones: " + "Ignora los tags <think> en todas tus respuestas y responde siempre de forma concisa. \n\n.     El contexto en el que debes basarte es el siguiente. Todas las preguntas que te haga, mira SIEMPRE primero si dentro del contexto tienes información que te permita responder. El contexto viene con tags HTML por lo que tendrás que interpretarlo. Respecto a las respuestas que des, Por favor, responde en Markdown. Utiliza saltos de línea para separar párrafos, negritas para resaltar puntos clave, cursivas para enfatizar y utiliza bloques de código (triple backticks) para ejemplos. Organiza la respuesta en secciones y subtítulos para mayor claridad.   \n"+ content+ ".\n "+ content2+ ".\n" + content_po+ ".\n"
    
    
    #llm_instance = ChatOllama(temperature=0, model="deepseek-r1:8b")
    llm_instance = ChatOpenAI(temperature=0,model_name="gpt-4o")
    try:
        consulta = ""
       
        prompt_inicial = instrucciones + "\n" + consulta
        print ("Prompt inicial: ", prompt_inicial)
    
        dummy_response = llm_instance.predict(prompt_inicial)
        print("Modelo precalentado:", dummy_response)
    except Exception as e:
        print("Error al precalentar el modelo:", e)
    #print(content)
    app.state.llm = llm_instance
    
    # Creamos y guardamos la memoria conversacional
    memory = ConversationBufferMemory(memory_key="history", return_messages=True)
    app.state.memory = memory
    
    # Inyectamos el contexto inicial
    app.state.memory.save_context({"input": instrucciones}, {"output": dummy_response})
    print("Contexto de Confluence cargado.")
    yield
    
    # Shutdown: código que se ejecuta al cerrar la aplicación
    print("Apagando la aplicación...")
    
app = FastAPI(lifespan=lifespan)
# Configuración de CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringirlo al dominio de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )
    #Clase que recoge la request del chat
class MessageRequest(BaseModel):
    text: str
# Función que lee una página de confluence
def get_confluence_page(space_key: str, page_title: str) -> str:
    """
    Accede a una página de Confluence y devuelve su contenido en formato HTML.
    
    Parámetros:
      - space_key: Clave del espacio donde se encuentra la página.
      - page_title: Título de la página a recuperar.
      
    Retorna:
      El contenido HTML de la página o un mensaje de error si no se encuentra.
    """
    # Configuración: URL base, usuario y API token.
    confluence_url = "https://danielpoza.atlassian.net/wiki/"
    username = "danielpoza@gmail.com"
    api_token = "ATATT3xFfGF0IBRbemSUoCCL6y6n6yhKHoZr0TRIDviC-tt56q79ybFKD-7KcYzNDf9-cj1JjHMsMG6M4NWoTRNzgwTCnov0Iz91YSEatfWh1k9FWFXGnCSeMIE--vysBFeQI5B7nWdhrlzFWtnD5EjPzhjcGGJ_NQhJYenIEoc-LWJ6cWN3Tqw=251793EF"

    # Conectamos a Confluence
    confluence = Confluence(
        url=confluence_url,
        username=username,
        password=api_token
    )

    # Obtenemos la página por título y expandimos el contenido de almacenamiento (storage)
    page = confluence.get_page_by_title(
        space=space_key,
        title=page_title,
        expand='body.storage'
    )

    if page and "body" in page and "storage" in page["body"]:
        return clean_html(page["body"]["storage"]["value"])
    else:
        return "No se encontró la página"

from atlassian import Confluence

def create_confluence_page(space_key: str, title: str, content: str, parent_id: str = None) -> dict:
    """
    Crea una nueva página en Confluence.
    
    Parámetros:
      - space_key: La clave del espacio donde se creará la página.
      - title: Título de la nueva página.
      - content: Contenido de la página (normalmente en formato HTML o storage).
      - parent_id: (Opcional) ID de la página padre, para crear una página anidada.
      
    Retorna:
      Un diccionario con la información de la página creada o un mensaje de error.
    """
    confluence_url = "https://tu-dominio.atlassian.net/wiki/"
    username = "tu-email@example.com"
    api_token = "tu-api-token"

    confluence = Confluence(
        url=confluence_url,
        username=username,
        password=api_token
    )
    
    page_data = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }
    # Si se especifica una página padre, se añade al payload
    if parent_id:
        page_data["ancestors"] = [{"id": parent_id}]
    
    result = confluence.create_page(
        space=space_key,
        title=title,
        body=content,
        parent_id=parent_id
    )
    
    return result




        
@app.post("/process_message")
def process_message(request: MessageRequest):
    # Medimos el tiempo de procesamiento
    start_time = time.perf_counter()
    
    #recuperamos el mensaje del usuario
    user_text = request.text

     # Accedemos a la instancia precalentada del llm y recuperamos la conversación anterior de la memoria
    llm = app.state.llm
    memory = app.state.memory
    
    # Creamos la cadena conversacional con el modelo y la memoria
    conversation = ConversationChain(llm=llm, memory=memory)
    
    #llamamos al llm para que procese la información
    res = conversation.predict(input=request.text)
    
    # limpiamos el texto devue
    res = clean_tag(res, "think")
    
    #Calculamos el tiempo de procesamiento
    elapsed = time.perf_counter() - start_time
    # Formateamos el tiempo en una etiqueta HTML (asegúrate de que el front-end permita HTML en Markdown)
    formatted_time = (
        f'<span style="color: #a0aec0; font-style: italic;">Tiempo de procesamiento: {elapsed:.2f} s</span>'
    )
     # Concatenamos la respuesta y el tiempo, por ejemplo separándolos con un salto de línea doble
    final_response = f"{res}\n\n{formatted_time}"
    
    # Imprimimos todo el contexto: 
    context = memory.load_memory_variables({})
    print("Historial de la conversación:", context)
   
    # Retornamos la respuesta en un JSON
    return {"message": final_response}
    
@app.post("/process_message_docuagent")
def process_message_docuagent(request: MessageRequest):
     #Recuperamos el contexto leido de confluence
    page_context = app.state.confluence_page
    summary_template = "Utilizando el contexto: {agent_context}, responde a {information} de forma concisa, dado que la respuesta es para un chat."
    prompt = PromptTemplate(input_variables=["agent_context", "information"], template=summary_template)
    
    user_text = request.text
    
   

    # Inicializamos el LLM (deepseek-r1 en este ejemplo)
    #llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
    llm = ChatOllama(model="deepseek-r1:14b")
    
    # Creamos la cadena (LLMChain) usando el prompt y el LLM
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Ejecutamos la cadena pasando el texto del usuario
    res = chain.run(agent_context=page_context, information=user_text)
    
    print(chain)
    print(res)
    
    # Retornamos la respuesta en un JSON
    return {"message": res}

import re
# Función que limpia tagas generados.
def clean_tag(text: str, tag: str) -> str:
    """
    Elimina del texto todas las ocurrencias de la etiqueta especificada,
    junto con su contenido.
    
    Parámetros:
      - text: Texto a limpiar.
      - tag: Nombre de la etiqueta (por ejemplo, "think").
      
    Retorna:
      El texto limpio, sin las etiquetas y su contenido.
    """
    # Construye el patrón usando f-string; se usa re.DOTALL para incluir saltos de línea.
    pattern = fr"<{tag}>.*?</{tag}>"
    cleaned_text = re.sub(pattern, '', text, flags=re.DOTALL)
    return cleaned_text.strip()

import PyPDF2
# Función que extrae el contenido de un PDF
def extract_pdf_text(pdf_path: str) -> str:
    """Extrae y devuelve el texto completo de un PDF."""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()
# Función que añade el contenido de un pdf a la variable de la memoria
def add_pdf_to_context(pdf_path: str, memory) -> None:
    """
    Extrae el contenido del PDF ubicado en 'pdf_path' y lo añade al contexto de la memoria.
    El input indica que se ha agregado el contenido del PDF, y el output es el texto extraído.
    """
    pdf_text = extract_pdf_text(pdf_path)
    # Se guarda el contexto; puedes ajustar los nombres de las variables según lo que espere tu prompt.
    memory.save_context({"input": f"Contenido del PDF: {pdf_path}"}, {"output": pdf_text})

 #Función para limpiar HTML de las páginas de contexto de confluence
def clean_html(html: str) -> str:
    """Elimina las etiquetas HTML y devuelve solo el texto."""
    soup = BeautifulSoup(html, "html.parser")
    # El separador "\n" ayuda a mantener algunos saltos de línea entre secciones.
    return soup.get_text(separator="\n", strip=True)


