import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class FnetSpider(scrapy.Spider):
    name = "fundos-net"

    def start_requests(self):
        yield scrapy.Request(
            url="https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM",
            callback=self.parse_page
        )

    def parse_page(self, response):
        service = Service(r"C:\Users\Vitor\Downloads\IC-FIIS\chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(service=service, options=options)

        try:
            driver.get(response.url)
            wait = WebDriverWait(driver, 15)
            time.sleep(5)

            wait.until(EC.element_to_be_clickable((By.ID, 'showFiltros'))).click()
            wait.until(EC.element_to_be_clickable((By.ID, "s2id_idFundo"))).click()
            campo_input = wait.until(EC.presence_of_element_located((By.ID, "s2id_autogen8")))
            campo_input.send_keys("ITAÚ ASSET RURAL FIAGRO - IMOBILIÁRIO")
            campo_input.send_keys(Keys.RETURN)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'select2-result-label') and contains(text(), 'ITAÚ ASSET')]"))).click()
            wait.until(EC.element_to_be_clickable((By.ID, 's2id_categoriaDocumento'))).click()
            campo_input_categoria = wait.until(EC.presence_of_element_located((By.ID, 's2id_autogen2_search')))
            campo_input_categoria.send_keys("Aviso aos Cotistas - Estruturado")
            campo_input_categoria.send_keys(Keys.RETURN)
            time.sleep(1)
            wait.until(EC.element_to_be_clickable((By.ID, "filtrar"))).click()
            time.sleep(5)
            wait.until(EC.presence_of_element_located((By.ID, "tblDocumentosEnviados")))
            time.sleep(5)

            paginas = driver.find_elements(By.CSS_SELECTOR, ".paginate_button[data-dt-idx]")
            indices_paginas = [int(btn.get_attribute("data-dt-idx")) for btn in paginas]

            for idx in indices_paginas:
                if idx != 1:
                    botao_pagina = wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, f'.paginate_button[data-dt-idx="{idx}"]'))
                    )
                    botao_pagina.click()
                    time.sleep(3)

                linhas = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
                for i in range(len(linhas)):
                    linhas = driver.find_elements(By.CSS_SELECTOR, "tbody tr")
                    linha = linhas[i]
                    celulas = linha.find_elements(By.TAG_NAME, "td")
                    if not celulas:
                        continue

                    link = celulas[-1].find_elements(By.CSS_SELECTOR, 'a[title="Visualizar Documento"]')
                    if not link:
                        continue

                    link[0].click()
                    time.sleep(2)
                    abas = driver.window_handles
                    driver.switch_to.window(abas[-1])

                    iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
                    driver.switch_to.frame(iframe)
                    wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")

                    rotulos = {
                        "data-base": "data_base",
                        "valor do provento": "valor_do_provento",
                        "data do pagamento": "data_do_pagamento",
                        "período de referência": "periodo_de_referencia"
                    }

                    dados = {}
                    for tr in soup.find_all("tr"):
                        tds = tr.find_all("td")
                        if len(tds) >= 2:
                            texto_rotulo = tds[0].get_text(strip=True).lower()
                            for chave in rotulos:
                                if chave in texto_rotulo:
                                    valor = tds[1].get_text(strip=True)
                                    dados[rotulos[chave]] = valor

                    if dados:
                        print("Dados para inserir no postgre",dados)
                        yield dados 

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(2)

        finally:
            driver.quit()
