#                             main.py
import pandas as pd
from tratardados import Tratamento
from classificadorAHP import ClassificacaoAHP
from scraper import OlxScraper

base_url = "https://www.olx.com.br/imoveis/aluguel/estado-mg/belo-horizonte-e-regiao?bas=1&bas=2&bas=3&bas=4&gsp=1&gsp=2&gsp=3&gsp=4&gsp=5&ros=1&ros=2&ros=3&ros=4&ros=5"
caminho = r'Projeto_OlxAluguel_scraping/dados/dados_olx_completo.xlsx'  

# scraperVar = OlxScraper(base_url, caminho)      Melhorar para o OlxScraper fazer a coletar_anuncios e exportar_dados tudo
# scraperVar.coletar_anuncios()
# scraperVar.exportar_dados(caminho)
# df=pd.read_excel(caminho) #lendo original

# necessario salvar uma copia sem os valores nulos, ela que usaremos
#df2 = df[df["Valor"] != "N/D"] #filtrando os anuncios sem valor no anuncio

caminho = r'Projeto_OlxAluguel_scraping/dados/dados_olx.xlsx'
#df2.to_excel(caminho, index=True) #salvando o df filtrado de valores de nulos
df2 = pd.read_excel(caminho) #lendo original

# #seu limite de alugel
valor_maximo=2500


filtrar = ClassificacaoAHP(df2, caminho)
df_pontuado = filtrar.pontuacao_final()
# Salvar o resultado
df_pontuado.to_excel("dados/anuncios_tratado.xlsx", index=True)

print(df_pontuado.sort_values("Pontuação Final:\n", ascending=False).head())

