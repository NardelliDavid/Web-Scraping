from django.shortcuts import render
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time
import json

# Función para scraping de mercadositio
def scrape_mercadositio():
    URL_base = "https://mercadositio.com/productos/celulares"
    li_items = []
    pagina = 1

    while True:
        URL = f"{URL_base}?page={pagina}"
        response = requests.get(URL)

        if response.status_code != 200:
            print(f"Error en la página: {URL}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        productos_encontrados = False

        for li in soup.find_all('li'): # Obtiene cada producto de la pagina
            img_tag = li.find('picture').find('img') if li.find('picture') else None
            title_tag = li.find('h2', class_='title')
            price_tag = li.find('span', class_='price-display')
            a_tag = li.find('a', href=True)

            img = img_tag['src'] if img_tag else None
            title = title_tag.text.strip() if title_tag else None
            price = price_tag.text.strip() if price_tag else None
            href = f"https://mercadositio.com{a_tag['href']}" if a_tag else None

            if title and price and href: # Agrega los productos al array
                li_items.append({'title': title, 'price': price, 'img': img, 'href': href, 'pagina': "Mercadositio"})
                productos_encontrados = True

        if not productos_encontrados:
            break

        pagina += 1

    return li_items

# Función para scraping de MercadoLibre
def scrape_mercadolibre(driver, urls):
    li_items = []

    for url in urls:
        try:
            driver.get(url)
            body = driver.find_element(By.TAG_NAME, "body")
            for _ in range(10):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.1)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            productos = soup.find_all('div', class_="andes-card")

            for producto in productos:
                img_tag = producto.find('img', class_='poly-component__picture')
                title_tag = producto.find('a', class_='poly-component__title', href=True)
                price_tag = producto.find('span', class_='andes-money-amount__fraction')

                img = img_tag['src'] if img_tag else None
                title = title_tag.text.strip() if title_tag else None
                price = price_tag.text.strip() if price_tag else None
                href = title_tag['href'] if title_tag else None

                if title and price and href:
                    li_items.append({'title': title, 'price': price, 'img': img, 'href': href, 'pagina': "Mercadolibre"})

        except Exception as e:
            print(f"Error al procesar {url}: {e}")

    return li_items

# Función para scraping de Xiaomi
def scrape_xiaomi(driver, urls):
    li_items = []

    for url in urls:
        try:
            driver.get(url)
            body = driver.find_element(By.TAG_NAME, "body")
            for _ in range(15):
                body.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.4)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            contenedor = soup.find('div', class_="products row products-grid")

            for producto in contenedor.find_all('div', class_="js-product-miniature-wrapper"):
                img_tag = producto.find('img', class_="img-fluid")
                title_tag = producto.find('h2', class_="h3 product-title")
                link_tag = title_tag.find('a') if title_tag else None
                price_tag = producto.find('div', class_="product-price-and-shipping").find('a')

                img = img_tag['src'] if img_tag else None
                title = link_tag.text.strip() if link_tag else None
                href = link_tag['href'] if link_tag else None
                price = price_tag.text.strip() if price_tag else None

                if title and price and href:
                    li_items.append({'title': title, 'price': price, 'img': img, 'href': href, 'pagina': "Xiaomi"})

        except Exception as e:
            print(f"Error al procesar {url}: {e}")

    return li_items

# Vista principal
def index(request):
    li_items = scrape_mercadositio()

    driver = webdriver.Chrome()
    try:
        meli_urls = [
            "https://www.mercadolibre.com.ar/mas-vendidos/MLA1055#origin=pdp",
            "https://www.mercadolibre.com.ar/mas-vendidos/MLA429749#origin=vip"
        ]
        li_items += scrape_mercadolibre(driver, meli_urls)

        xiaomi_urls = [
            "https://xiaomistore.com.ar/11-smartphones?order=product.price.asc&q=Categor%C3%ADas-Redmi-Redmi+Note/Disponibilidad-En+stock",
            "https://xiaomistore.com.ar/261-cargadores-?order=product.position.asc&productListView=grid"
        ]
        li_items += scrape_xiaomi(driver, xiaomi_urls)

    finally:
        driver.quit()

    # Transforma el array a JSON
    li_items_json = json.dumps(li_items)

    # Renderiza la plantilla
    return render(request, 'index.html', {'li_items': li_items, 'li_items_json': li_items_json})
