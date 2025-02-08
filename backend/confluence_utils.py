# Importaciones necesarias
from atlassian import Confluence
import os
from bs4 import BeautifulSoup

confluence_url = "https://danielpoza.atlassian.net/wiki/"
username = "danielpoza@gmail.com"
api_token = "ATATT3xFfGF0IBRbemSUoCCL6y6n6yhKHoZr0TRIDviC-tt56q79ybFKD-7KcYzNDf9-cj1JjHMsMG6M4NWoTRNzgwTCnov0Iz91YSEatfWh1k9FWFXGnCSeMIE--vysBFeQI5B7nWdhrlzFWtnD5EjPzhjcGGJ_NQhJYenIEoc-LWJ6cWN3Tqw=251793EF"

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
    #confluence_url = "https://danielpoza.atlassian.net/wiki/"
    #username = "danielpoza@gmail.com"
    #api_token = "ATATT3xFfGF0IBRbemSUoCCL6y6n6yhKHoZr0TRIDviC-tt56q79ybFKD-7KcYzNDf9-cj1JjHMsMG6M4NWoTRNzgwTCnov0Iz91YSEatfWh1k9FWFXGnCSeMIE--vysBFeQI5B7nWdhrlzFWtnD5EjPzhjcGGJ_NQhJYenIEoc-LWJ6cWN3Tqw=251793EF"

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
    
    #Lectura parámetros: 
    print("\n\n ***\n *** CREAR PAGINA CONFLUENCE \n ***\n\n")
    print ("Creando página", title, " en ", space_key, " bajo ", title, "\n\n")
    print("\nURL:", confluence_url, "\nUSER NAME: ", username, "\nPASSWORD", api_token)
    
    confluence = Confluence(
        url=confluence_url,
        username=username,
        password=api_token,
        cloud=True
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
        
    print("\n Datos de la página: \n", page_data)
     # Primero, intentamos obtener la página por título
    existing_page = confluence.get_page_by_title(space=space_key, title=title)
    
    if existing_page:
        page_id = existing_page["id"]
        # Actualizamos la página existente. 
        # Nota: update_page se encarga de incrementar la versión automáticamente.
        updated_page = confluence.update_page(
            page_id=page_id,
            title=title,
            body=content,
            representation="storage",
            minor_edit=True
        )
        return updated_page
    else:  
        result = confluence.create_page(
            space=space_key,
            title=title+"IABOT",
            body=content,
            parent_id=parent_id
        )
    
    return result

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

 #Función para limpiar HTML de las páginas de contexto de confluence
def clean_html(html: str) -> str:
    """Elimina las etiquetas HTML y devuelve solo el texto."""
    soup = BeautifulSoup(html, "html.parser")
    # El separador "\n" ayuda a mantener algunos saltos de línea entre secciones.
    return soup.get_text(separator="\n", strip=True)