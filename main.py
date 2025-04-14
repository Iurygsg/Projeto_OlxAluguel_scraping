# main.py
from scraper import OlxScraper
import pandas as pd
from tratardados import Tratamento
import time
base_url = "https://www.olx.com.br/imoveis/aluguel/estado-mg/belo-horizonte-e-regiao?bas=1&bas=2&bas=3&bas=4&gsp=1&gsp=2&gsp=3&gsp=4&gsp=5&ros=1&ros=2&ros=3&ros=4&ros=5"
caminho = r'dados/dados_olx.xlsx'  

# scraperVar = OlxScraper(base_url)
# scraperVar.coletar_anuncios()
# scraperVar.exportar_dados(caminho)
df=pd.read_excel('Projeto_OlxAluguel_scraping/'+ caminho)

# Aplicar tratamento
tratamento = Tratamento(df)
df_tratado = tratamento.processar()

# Salvar o resultado
df_tratado.to_excel("dados/anuncios_tratado.xlsx", index=False)