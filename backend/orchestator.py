from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from ollama import chat
import os

# Cargar las variables del archivo .env
load_dotenv()
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI

# Inicializar el modelo con memoria
memory = ConversationBufferMemory()

llm = ChatOpenAI(
    model_name="gpt-4-turbo",
    temperature=0
)

# Crear una cadena de conversación con memoria
conversation = ConversationChain(
    llm=llm,
    memory=memory
)

# Primera interacción
print(conversation.predict(input="Hola, me llamo Juan."))
# Respuesta: "¡Hola Juan! ¿En qué puedo ayudarte hoy?"

# Segunda interacción (el modelo recuerda el contexto)
print(conversation.predict(input="¿Cómo me llamo?"))
# Respuesta: "Te llamas Juan."

