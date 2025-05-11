# scraper.py
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from datetime import datetime, timedelta
from selenium.webdriver.firefox.service import Service
import re

class OlxScraper:
    def __init__(self, base_url, caminho):
        self.base_url = base_url
        self.lista_anuncios = []
        self.driver = self.setup_driver()
        self.caminho = caminho

    def setup_driver(self):
        FIREFOX_EXECUTABLE = os.getenv('FIREFOX_EXECUTABLE', r'C:\Users\iurex\AppData\Local\Mozilla Firefox\firefox.exe')
        GECKODRIVER_EXECUTABLE = os.getenv('GECKODRIVER_EXECUTABLE', r'C:\Users\iurex\Documents\Puc\Tcc I\geckodriver.exe')
    
        options = webdriver.FirefoxOptions()
        options.binary_location = FIREFOX_EXECUTABLE
    
        service = Service(executable_path=GECKODRIVER_EXECUTABLE)
        return webdriver.Firefox(service=service, options=options)
    
    def tratar_data_publicacao(self, data_texto):
        hoje = datetime.today().date()
        if "Hoje" in data_texto:
            return hoje.strftime('%d/%m/%Y')
        elif "Ontem" in data_texto:
            return (hoje - timedelta(days=1)).strftime('%d/%m/%Y')
        return data_texto

    def obter_ultima_pagina(self, soup):
        ultima_pagina_elemento = soup.find("button", {"class": "olx-core-button olx-core-button--link olx-core-button--small"}, string="Última página")
        if ultima_pagina_elemento:
            link_tag = ultima_pagina_elemento.find("a")
            if link_tag:
                link = link_tag['href']
                return int(link.split('&o=')[-1])
        return 3  # valor padrão

    def coletar_anuncios(self):
        # sua lógica aqui...
        self.driver.get(self.base_url)
        time.sleep(random.randint(5, 15))

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        ultima_pagina = self.obter_ultima_pagina(soup)

        for pagina in range(1, ultima_pagina + 1):
            try:
                print(f"Coletando dados da página {pagina}...")
                self.driver.get(f"{self.base_url}&o={pagina}")
                time.sleep(random.randint(5, 15))
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'lxml')

                anuncios = soup.find_all("section", {"class": "AdCard_root__Jkql_ AdCard_horizontal__hrnuP"})
                if not anuncios:
                    print(f"Nenhum anúncio encontrado na página {pagina}.")
                    break

                for anuncio in anuncios:
                    self.processar_anuncio(anuncio)
                    dlen=len(self.lista_anuncios)
                print("Totais dados coletados:",dlen)

            except Exception as e:
                print(f"Erro na página {pagina}: {e}")
                continue

        self.driver.quit()
        pass

    def processar_anuncio(self, anuncio):
        try:
            titulo = anuncio.find("h2", {"data-ds-component": "DS-Text"})
            preco = anuncio.find("h3", {"data-ds-component": "DS-Text"})
            link = anuncio.find("a", {"class": "AdCard_link__4c7W6"})
            local = anuncio.find("p", {"class": "olx-text olx-text--caption olx-text--block olx-text--regular AdCard_location__NGMql"})
            data = anuncio.find("p", {"class": "olx-text olx-text--caption olx-text--block olx-text--regular AdCard_date__KCWNe"})

            info = {
                "Título": titulo.text.strip() if titulo else "N/D",
                "Valor": preco.text.strip() if preco else "N/D",
                "URL": link['href'] if link else "N/D",
                "Localizacao": local.text.strip() if local else "N/D",
                "Data publicada": self.tratar_data_publicacao(data.text.strip()) if data else "N/D"
            }

            self.lista_anuncios.append(info)

        except Exception as e:
            print("Erro ao processar anúncio:", e)

    def exportar_dados(self):
        df = pd.DataFrame(self.lista_anuncios)
        df["Valor"] = df["Valor"].apply(lambda x : re.sub(r'[^\d,]', '', x).replace(',','.'))
        df["Valor"] = pd.to_numeric(df["Valor"], errors='coerce')
        df["Valor"] = df["Valor"].astype(float)
        df.to_excel(self.caminho, index=True)
