from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests, time

def index(request):
    # ------------------------------------------------------------------------------------------------------------------------------------------
    # Scraping a mercadositio
    URL_base = "https://mercadositio.com/productos/celulares"
    
    li_items = [] # Lista para almacenar los productos
    pagina = 1  # Pagina en la que debe iniciar a scrapear
    
    while True:
        URL = f"{URL_base}?page={pagina}" # URL donde iniciara el script
        
        # Obtener el contenido de la página
        resultado = requests.get(URL)
        
        # Si no hay respuesta exitosa (200), salir del ciclo
        if resultado.status_code != 200:
            print("Error en la pagina")
            break
        
        soup = BeautifulSoup(resultado.text, 'html.parser')
        
        # Extraer los productos de la página
        productos_encontrados = False
        for li in soup.find_all('li'):
            div_tag = li.find('div', class_='hover')
            img_tag = div_tag.find('img') if div_tag else None
            if not img_tag: # En caso de que no exista el img tag
                div_tag = li.find('picture') # Busca la etiqueta picture
                img_tag = div_tag.find('img') if div_tag else None # Busca la imagen
            img = img_tag['src'] if img_tag else None
            
            title_tag = li.find('h2', class_='title') # Obtiene el titulo del producto
            title = title_tag.text if title_tag else None
            
            price_tag = li.find('span', class_='price-display') # Obtiene el precio del producto
            price = price_tag.text if price_tag else None
            
            a_tag = li.find('a', href=True) # Obtiene la url hacia el producto
            href = a_tag['href'] if a_tag else None
            if href: # Si existe la url la concatena
                href = "https://mercadositio.com"+href
            
            if title and price and href: # Agrega el producto solo si existe titulo, precio y link al producto
                li_items.append({'title': title, 'price': price, 'img': img, 'href': href, 'pagina': "Mercadositio"})
                productos_encontrados = True
        
        # Si no se encontraron productos en esta página, significa que no hay más páginas
        if not productos_encontrados:
            print("--------No hay mas paginas a scrapear (mercadositio)--------")
            break
        
        # Avanzar a la siguiente página
        pagina += 1
    
    # ------------------------------------------------------------------------------------------------------------------------------------------
    # Scraping a mercadolibre (20 mas vendidos)
    URL_MELI_CELUS = "https://www.mercadolibre.com.ar/mas-vendidos/MLA1055#origin=pdp"
    URL_MELI_CABLES = "https://www.mercadolibre.com.ar/mas-vendidos/MLA429749#origin=vip"
    
    URLS_MELI = [URL_MELI_CELUS, URL_MELI_CABLES]
    
    # Abre el navegador
    driver = webdriver.Chrome()
    
    for url in URLS_MELI:
        try:
            driver.get(url) # Entra en el navegador a la url de mercadolibre
            # Realiza scroll en mercadolibre para cargar las imagenes correctamente
            body = driver.find_element(By.TAG_NAME, "body")
            for _ in range(10):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.1)
                
            # Extrae el html de la pagina despues de cargarse
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            # Div que almacena todos los productos
            clasesDiv = "andes-card ui-search-layout--grid__item poly-card poly-card--grid-card andes-card--flat andes-card--padding-0 andes-card--animated"
            for div in soup.find_all('div', class_=clasesDiv):
                # Busca la imagen de portada
                div_tag = div.find('div', class_='poly-card__portada')
                img_tag = div_tag.find('img', class_='poly-component__picture') if div_tag else None
                img = img_tag['src'] if img_tag else None
                # Busca el titulo del producto
                title_tag = div.find('a', class_='poly-component__title', href=True)
                title = title_tag.text if title_tag else None
                # Busca el precio del producto
                price_tag = div.find('span', class_='andes-money-amount__fraction')
                price = price_tag.text if price_tag else None
                # Busca la url del producto
                href = title_tag['href'] if title_tag else None
                
                if title and price and href: # Agrega el producto solo si existe titulo, precio y link al producto
                    li_items.append({'title': title, 'price': price, 'img': img, 'href': href, 'pagina': "Mercadolibre"})
        except Exception as e:
                print(f"Error al cargar la página: {e}")
                print(f"Detalles del error: {str(e)}")
    
    # ------------------------------------------------------------------------------------------------------------------------------------------
    URL_XIAOMI_CELULARES = "https://xiaomistore.com.ar/11-smartphones?order=product.price.asc&q=Categor%C3%ADas-Redmi-Redmi+Note/Disponibilidad-En+stock"
    URL_XIAOMI_CARGADORES = "https://xiaomistore.com.ar/261-cargadores-?order=product.position.asc&productListView=grid"
    
    URLS_XIAOMI = [URL_XIAOMI_CELULARES, URL_XIAOMI_CARGADORES]
    
    for url in URLS_XIAOMI:
        try:
            driver.get(url) # Entra en el navegador a la url de xiaomi
            # Realiza scroll en xiaomi para cargar las imagenes correctamente
            body = driver.find_element(By.TAG_NAME, "body")
            for _ in range(15):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.4)
                    
            # Extrae el html de la pagina despues de cargarse
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Contenedor de los productos
            contenedor = soup.find('div', class_="products row products-grid")
            # Obtiene los datos de cada producto
            for producto in contenedor.find_all('div', class_="js-product-miniature-wrapper"): # Producto 1 por 1
                # Imagen del producto
                img_tag = producto.find('img', class_="img-fluid js-lazy-product-image lazy-product-image product-thumbnail-first entered loaded") if div_tag else None
                img = img_tag['src'] if img_tag else None
                # Titulo
                title_tag = producto.find('h2', class_="h3 product-title")
                link_tag = title_tag.find('a') if title_tag else None
                title = link_tag.text if link_tag else None
                # Link
                link = link_tag['href'] if link_tag else None
                # Precio
                price_tag = producto.find('div', class_="product-price-and-shipping")
                price_t = price_tag.find('a') if price_tag else None
                price = price_t.text if price else None
                
                if title and price and link: # Agrega el producto solo si existe titulo, precio y link al producto
                    li_items.append({'title': title, 'price': price, 'img': img, 'href': link, 'pagina': "Xiaomi"})
        except Exception as e:
            print("Error")
    driver.quit() # Cierra el navegador
    
    # Pasar los productos a la plantilla
    return render(request, "index.html", {"li_items": li_items})