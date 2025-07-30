#Imports necessários
#Selenium: Simula um navegador web para acessar páginas
#BeautifulSoup: Facilita a extração de dados de HTML e XML
#WebDriverManager: Gerencia o driver do navegador automaticamente

# Imports necessários
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
from colorama import init, Fore, Style
init(autoreset=True)  # Inicializa o colorama para resetar cores automaticamente

# Definição da URL do produto
urls = [
    "https://www.terabyteshop.com.br/produto/34884/placa-de-video-gigabyte-nvidia-geforce-rtx-5070-gaming-oc-12gb-gddr7-dlss-ray-tracing-gv-n5070gaming-oc-12gd",
    "https://www.kabum.com.br/produto/714574/placa-de-video-gigabyte-rtx-5070-windforce-oc-sff-12g-nvidia-geforce-12gb-gddr7-192bits-dlss-ray-tracing-9vn5070wo-00-g10",
    "https://www.pichau.com.br/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bit-gv-n5070gaming-oc-12gd",
    "https://www.terabyteshop.com.br/produto/28037/water-cooler-gigabyte-aorus-waterforce-ii-360-argb-360mm-intel-amd-black",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/products")
def get_products():
    try:
        with open("products.json", encoding="utf-8") as f:
            products = json.load(f)
        return products
    except Exception as e:
        return {"error": str(e)}

def scraping_loop():
    while True:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--log-level=3")  # Apenas erros graves
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Remove logs do driver
        service = Service(ChromeDriverManager().install(), log_path='NUL')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print(Fore.BLUE + "Iniciando o scraping...")
        for url in urls:
            print(Fore.MAGENTA + f"Acessando a URL: {url}")
            driver.get(url)
            driver.implicitly_wait(5)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            if "terabyteshop" in url:
                name = soup.find('h1', class_='tit-prod')
                name_product = name.text.strip() if name else "Nome não encontrado"
                price = soup.find('p', class_='val-prod valVista') or soup.find('h2', class_='val-prod valVista') or soup.find('i', class_='fa fa-exclamation-circle')
                valor_produto = price.text.strip() if price else "Preço não encontrado"
            elif "kabum" in url:
                name = soup.find('h1', class_='text-sm desktop:text-xl text-black-800 font-bold desktop:font-bold')
                name_product = name.text.strip() if name else "Nome não encontrado"
                price = soup.find('h4', class_='text-4xl text-secondary-500 font-bold transition-all duration-500')
                valor_produto = price.text.strip() if price else "Preço não encontrado"
            elif "pichau" in url:
                name = soup.find('h1', class_='MuiTypography-root MuiTypography-h6 mui-vrkxks-product_info_title')
                name_product = name.text.strip() if name else "Nome não encontrado"
                price = soup.find('div', class_='mui-1q2ojdg-price_vista')
                valor_produto = price.text.strip() if price else "Preço não encontrado"
            else:
                name = None
                price = None
                name_product = "Nome não encontrado"
                valor_produto = "Preço não encontrado"

            data = {
                "nome": name_product,
                "preco": valor_produto,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "site": url.split('/')[2],
                "link": url,
            }

            try:
                with open("products.json", "r", encoding="utf-8") as f:
                    lista = json.load(f)
                    if not isinstance(lista, list):
                        lista = []
            except (FileNotFoundError, json.JSONDecodeError):
                lista = []

            if not any(item['preco'] == valor_produto and item['nome'] == name_product for item in lista):
                lista.append(data)

            with open("products.json", "w", encoding="utf-8") as f:
                json.dump(lista, f, ensure_ascii=False, indent=4)

            print(Fore.GREEN + f"Dados salvos com sucesso! Nome do produto: {name_product} - Preço: {valor_produto} - Site: {url.split('/')[2]}")
            time.sleep(5)
        driver.quit()
        time.sleep(5)
        print(Fore.YELLOW + "Aguardando 5 segundos antes de reiniciar o loop...")

# Inicia o scraping em uma thread ao iniciar o FastAPI
threading.Thread(target=scraping_loop, daemon=True).start()

