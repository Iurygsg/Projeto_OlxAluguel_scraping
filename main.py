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
df=pd.read_excel('Projeto_OlxAluguel_scraping/dados/dados_olx.xlsx')

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
# Inicializa o geolocalizador
geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0")

# Coordenadas de referência do bairro Padre Eustáquio, BH
local_referencia = "Belo Horizonte"
def geocode_with_retry(local_referencia, tentativas=3):
    for i in range(tentativas):
        try:
            return geolocator.geocode(local_referencia, timeout=10)
        except :
            print(f"Tentativa {i+1} falhou. Tentando novamente...")
            time.sleep(2)
    return None
local_ref_coords = geocode_with_retry(local_referencia)
print(local_ref_coords)