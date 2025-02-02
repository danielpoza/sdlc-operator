from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configura CORS para permitir comunicación con React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL de tu frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

@app.post("/process-message")
async def process_message(request: MessageRequest):
    try:
        # Aquí va tu lógica Python
        result = tu_funcion_python(request.message)
        
        return {
            "original": request.message,
            "processed": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def tu_funcion_python(texto: str):
    """Ejemplo: función de procesamiento"""
    # Puedes poner cualquier lógica aquí:
    # - LLM (ChatGPT)
    # - Análisis de sentimientos
    # - Conexión a bases de datos
    # - Cálculos complejos
    
    return f"Procesado en Python: {texto.upper()}"

# Para ejecutar: uvicorn main:app --reload