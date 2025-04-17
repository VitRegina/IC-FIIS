from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

import pandas as pd

navegador = webdriver
service = Service(r"C:\Users\Vitor\Downloads\IC-FIIS\chromedriver.exe")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

url = "https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM"
driver.get(url)

time.sleep(5)

exibir_filtro = WebDriverWait(driver, 10).until( 
    EC.presence_of_element_located((By.ID, 'showFiltros'))
)
exibir_filtro.click()


WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "s2id_idFundo"))
).click()

campo_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "s2id_autogen8"))
)
campo_input.send_keys("ITAÚ ASSET RURAL FIAGRO - IMOBILIÁRIO")
campo_input.send_keys(Keys.RETURN)


WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'select2-result-label') and contains(text(), 'ITAÚ ASSET')]"))
).click()

WebDriverWait(driver, 10).until(
  EC.element_to_be_clickable((By.ID, 's2id_categoriaDocumento'))

).click()

campo_input_categoria = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, 's2id_autogen2_search'))
)
campo_input_categoria.send_keys("Aviso aos Cotistas - Estruturado")
campo_input_categoria.send_keys(Keys.RETURN)
time.sleep(1)  

WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "filtrar"))
).click()

time.sleep(5)

tabela = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "tblDocumentosEnviados"))
)

time.sleep(5)

linhas = tabela.find_elements(By.CSS_SELECTOR, "tbody tr")

dados_gerais = []

for linha in linhas:
    try:
        ultima_celula = linha.find_elements(By.TAG_NAME, "td")[-1]
        ultima_celula.click()

        link = ultima_celula.find_element(By.CSS_SELECTOR, 'a[title="Visualizar Documento"]')
        link.click()

        print("88")
        time.sleep(2)

        abas = driver.window_handles

        driver.switch_to.window(abas[-1])

        iframe = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )

        print('95')

        driver.switch_to.frame(iframe)


        WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        rotulos = {
            "Data base": "Data base",
            "valor do provento" : "valor do provento",
            "data do pagamento" : "data do pagamento",
            "período de referência" : "período de referência"
        }
        print("104")

        dados = {}

        print("110")

        for tr in soup.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) >= 2:
                texto_rotulo = tds[0].get_text(strip=True).lower()
                for chave in rotulos:
                    if chave in texto_rotulo:
                        valor = tds[1].get_text(strip=True)
                        print(f" Match: {chave} => {valor}")
                        dados[rotulos[chave]] = valor

        print("121")

        dados_gerais.append(dados)
        driver.back()
        time.sleep(3)

        for k,v in dados.items():
            print("124")
            print(f"{k}: {v}")
    except Exception as e:
        print(f"Erro {e}")
        continue


df=pd.DataFrame(dados_gerais)

caminho_arquivo = r"C:\Users\Vitor\Downloads\IC-FIIS\Relatório.xlsx"

df.to_excel(caminho_arquivo, index=False)

driver.quit()