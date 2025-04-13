# main.py
from scraper import OlxScraper

base_url = "https://www.olx.com.br/imoveis/aluguel/estado-mg/belo-horizonte-e-regiao?bas=1&bas=2&bas=3&bas=4&gsp=1&gsp=2&gsp=3&gsp=4&gsp=5&ros=1&ros=2&ros=3&ros=4&ros=5"
caminho = r'dados/dados_olx.xlsx'  # ou coloque o caminho absoluto se preferir

scraper = OlxScraper(base_url)
scraper.coletar_anuncios()
scraper.exportar_dados(caminho)
