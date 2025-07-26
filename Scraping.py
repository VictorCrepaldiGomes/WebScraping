#Imports necessários
#Selenium: Simula um navegador web para acessar páginas
#BeautifulSoup: Facilita a extração de dados de HTML e XML
#WebDriverManager: Gerencia o driver do navegador automaticamente

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json

#Definição da URL do produto
urls = [
    "https://www.terabyteshop.com.br/produto/34884/placa-de-video-gigabyte-nvidia-geforce-rtx-5070-gaming-oc-12gb-gddr7-dlss-ray-tracing-gv-n5070gaming-oc-12gd",
    "https://www.kabum.com.br/produto/714574/placa-de-video-gigabyte-rtx-5070-windforce-oc-sff-12g-nvidia-geforce-12gb-gddr7-192bits-dlss-ray-tracing-9vn5070wo-00-g10",
    "https://www.pichau.com.br/placa-de-video-gigabyte-geforce-rtx-5070-gaming-oc-12gb-gddr7-192-bit-gv-n5070gaming-oc-12gd",
    "https://www.terabyteshop.com.br/produto/28037/water-cooler-gigabyte-aorus-waterforce-ii-360-argb-360mm-intel-amd-black",

]
#Criação de um loop infinito para monitorar a página

while True:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    for url in urls:
        print(f"Acessando a URL: {url}")
        #Abre o navegador e acessa a URL
        driver.get(url)
        driver.implicitly_wait(5)

        #Extrai o conteúdo HTML da página (HTML BRUTO, por isso seria necessário usar o Selenium para interagir com a página)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        #Adaptando urls para selecionar o produto do site correto
        #Extrai o nome e o preço do produto(É necessário verificar os elementos diretos no console da página)

        if "terabyteshop" in url:
            name = soup.find('h1', class_='tit-prod')
            name_product = name.text.strip() if name else "Nome não encontrado"
            price = soup.find('p', class_='val-prod valVista') or soup.find('h2', class_='val-prod valVista') or soup.find('i', class_='fa fa-exclamation-circle')
            valor_produto = price.text.strip() if price else "Preço não encontrado"

        
        elif "kabum" in url:
            name = soup.find('h1', class_='text-sm desktop:text-xl text-black-800 font-bold desktop:font-bold')  # Ajuste se o nome do produto estiver em outro lugar
            name_product = name.text.strip() if name else "Nome não encontrado"
            price = soup.find('h4', class_='text-4xl text-secondary-500 font-bold transition-all duration-500')
            valor_produto = price.text.strip() if price else "Preço não encontrado"

        elif "pichau" in url:
            name = soup.find('h1', class_='MuiTypography-root MuiTypography-h6 mui-vrkxks-product_info_title')  # Ajuste se o nome do produto estiver em outro lugar
            name_product = name.text.strip() if name else "Nome não encontrado"
            price = soup.find('div', class_='mui-1q2ojdg-price_vista')
            valor_produto = price.text.strip() if price else "Preço não encontrado"

        elif "kabum" in url:
            name = soup.find('h1', class_='text-sm desktop:text-xl text-black-800 font-bold desktop:font-bold')  # Ajuste se o nome do produto estiver em outro lugar
            name_product = name.text.strip() if name else "Nome não encontrado"
            price = soup.find('h4', class_='text-4xl text-secondary-500 font-bold transition-all duration-500')
            valor_produto = price.text.strip() if price else "Preço não encontrado"

        elif "kabum" in url:
            name = soup.find('h1', class_='text-sm desktop:text-xl text-black-800 font-bold desktop:font-bold')  # Ajuste se o nome do produto estiver em outro lugar
            name_product = name.text.strip() if name else "Nome não encontrado"
            price = soup.find('h4', class_='text-4xl text-secondary-500 font-bold transition-all duration-500')
            valor_produto = price.text.strip() if price else "Preço não encontrado"    

        else: 
            name = None
            price = None
        name_product = name.text.strip() if name else "Nome não encontrado"
        valor_produto = price.text.strip() if price else "Preço não encontrado"


        #Extrai o nome e o preço do produto(É necessário verificar os elementos diretos no console da página)


        #Cria um dicionário com os dados do produto, para salvar em um arquivo JSON
        data = {
            "nome": name_product,
            "preco": valor_produto,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "site": url.split('/')[2],
            "link": url,
        }

        #Tenta abrir o arquivo JSON e carregar os dados existentes
        #Se o arquivo não existir ou estiver vazio, cria uma nova lista
        #Adiciona os novos dados à lista e salva de volta no arquivo JSON

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

        print(f"Dados salvos com sucesso! Nome do produto: {name_product} - Preço: {valor_produto} - Site: {url.split('/')[2]}")
        time.sleep(5)
    driver.quit()
    time.sleep(5)
    print("Aguardando 5 segundos antes de reiniciar o loop...")

