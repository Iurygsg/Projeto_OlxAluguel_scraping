# main.py
import pandas as pd
from tratardados import Tratamento

base_url = "https://www.olx.com.br/imoveis/aluguel/estado-mg/belo-horizonte-e-regiao?bas=1&bas=2&bas=3&bas=4&gsp=1&gsp=2&gsp=3&gsp=4&gsp=5&ros=1&ros=2&ros=3&ros=4&ros=5"
caminho = r'dados/dados_olx.xlsx'  

# scraperVar = OlxScraper(base_url)
# scraperVar.coletar_anuncios()
# scraperVar.exportar_dados(caminho)
df=pd.read_excel('Projeto_OlxAluguel_scraping/'+ caminho)
valor_maximo=2500
# Aplicar tratamento
tratar = Tratamento(df, valor_maximo)
df_tratado = tratar.processar()

# Salvar o resultado
df_tratado.to_excel("dados/anuncios_tratado.xlsx", index=True)

#Classificação a baixo

