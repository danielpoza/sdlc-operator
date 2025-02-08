from atlassian import Confluence
# curl -v https://danielpoza.atlassian.net/wiki --user danielpoza@gmail.com:ATATT3xFfGF0IBRbemSUoCCL6y6n6yhKHoZr0TRIDviC-tt56q79ybFKD-7KcYzNDf9-cj1JjHMsMG6M4NWoTRNzgwTCnov0Iz91YSEatfWh1k9FWFXGnCSeMIE--vysBFeQI5B7nWdhrlzFWtnD5EjPzhjcGGJ_NQhJYenIEoc-LWJ6cWN3Tqw=251793EF
def create_confluence_page():
    # Configuración de conexión a Confluence
    confluence_url = "https://danielpoza.atlassian.net/wiki/"
    username = "danielpoza@gmail.com"
    api_token = "ATATT3xFfGF0IBRbemSUoCCL6y6n6yhKHoZr0TRIDviC-tt56q79ybFKD-7KcYzNDf9-cj1JjHMsMG6M4NWoTRNzgwTCnov0Iz91YSEatfWh1k9FWFXGnCSeMIE--vysBFeQI5B7nWdhrlzFWtnD5EjPzhjcGGJ_NQhJYenIEoc-LWJ6cWN3Tqw=251793EF"
    
    # Define el espacio donde se creará la página
    space_key = "CS"
    
    # Define el título y el contenido HTML de la nueva página
    title = "Página de prueba creada desde script"
    content = (
        "<h1>Hola, esta es una página de prueba</h1>"
        "<p>Creada a través de la API de Confluence.</p>"
    )
    
    # Conecta con Confluence
    confluence = Confluence(
        url=confluence_url,
        username=username,
        password=api_token,
        cloud=True
    )
    
    
    try:
        # Crea la página sin establecer un ancestro (para una página raíz)
        result = confluence.create_page(
            space=space_key,
            title=title,
            body=content
        )
        print("Página creada exitosamente:")
        print(result)
    except Exception as e:
        print("Error al crear la página:")
        print(e)

if __name__ == "__main__":
    create_confluence_page()
