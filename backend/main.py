# /app/backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain import PromptTemplate, LLMChain
from contextlib import asynccontextmanager

# Importa el módulo o la clase de LangChain que necesites.
# Aquí usamos OpenAI como ejemplo.
from langchain_community.llms import OpenAI
from ollama import chat
from pydantic import BaseModel
from atlassian import Confluence  
import os


load_dotenv()
summary_template = ""

#Función que se ejecutará al inicializar el servidor: 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: código que se ejecuta al iniciar la aplicación
    print("INICIO SERVICIO BACKEND SDLC OPERATOR")
    content = get_confluence_page("CS", "ArquitecturaServicios")
    print(content)
    app.state.confluence_page = content
    yield
    # Shutdown: código que se ejecuta al cerrar la aplicación
    print("Apagando la aplicación...")
    
app = FastAPI(lifespan=lifespan)

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
        return page["body"]["storage"]["value"]
    else:
        return "No se encontró la página"


    
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
@app.post("/process_message")
def process_message(request: MessageRequest):
     #Recuperamos el contexto leido de confluence
    page_context = app.state.confluence_page
    summary_template = "Utilizando el contexto: {agent_context}, responde a {information} de forma concisa, dado que la respuesta es para un chat."
    prompt = PromptTemplate(input_variables=["agent_context", "information"], template=summary_template)
    
    user_text = request.text
    
   

    # Inicializamos el LLM (ChatOpenAI en este ejemplo)
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
    
    # Creamos la cadena (LLMChain) usando el prompt y el LLM
    chain = LLMChain(llm=llm, prompt=prompt)
    
    # Ejecutamos la cadena pasando el texto del usuario
    res = chain.run(agent_context=page_context, information=user_text)
    
    print(chain)
    print(res)
    
    # Retornamos la respuesta en un JSON
    return {"message": res}
    
    
