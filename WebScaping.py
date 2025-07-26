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
url = "https://www.terabyteshop.com.br/produto/34884/placa-de-video-gigabyte-nvidia-geforce-rtx-5070-gaming-oc-12gb-gddr7-dlss-ray-tracing-gv-n5070gaming-oc-12gd"

#Criação de um loop infinito para monitorar a página
while True:

    #Abre o navegador e acessa a URL
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)
    driver.implicitly_wait(5)

    #Extrai o conteúdo HTML da página (HTML BRUTO, por isso seria necessário usar o Selenium para interagir com a página)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #Extrai o nome e o preço do produto(É necessário verificar os elementos diretos no console da página)
    name = soup.find('h1', class_='tit-prod')
    name_product = name.text.strip() if name else "Nome não encontrado"

    price = soup.find('p', class_='val-prod valVista')
    valor_produto = price.text.strip() if price else "Preço não encontrado"

    #Cria um dicionário com os dados do produto, para salvar em um arquivo JSON
    data = {
        "nome": name_product,
        "preco": valor_produto,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
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

    lista.append(data)

    with open("products.json", "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=4)

    print("Dados salvos com sucesso!", data)

    driver.quit()
    time.sleep(1)