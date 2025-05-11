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
df=pd.read_excel(caminho) #lendo original

# necessario salvar uma copia sem os valores nulos, ela que usaremos
df_filtrado = df[df["Valor"] != "N/D"] #filtrando os anuncios sem valor no anuncio

caminho = r'Projeto_OlxAluguel_scraping/dados/dados_olx.xlsx'
df_filtrado.to_excel(caminho, index=True) #salvando o df filtrado de valores de nulos
df_filtrado=pd.read_excel(caminho) #lendo original

# #seu limite de alugel
valor_maximo=2500

# # Aplicar tratamento
tratar = Tratamento(df_filtrado, valor_maximo)
df_filtrado = tratar.processar()
filtrar = ClassificacaoAHP(df_filtrado)
df_filtrado = filtrar.pontuacao_final()
 # Salvar o resultado
df_filtrado.to_excel("dados/anuncios_tratado.xlsx", index=True)

print("Ranking final dos anúncios (maior é melhor):\n")
print(df_filtrado)
print("o maior é:\n", max(df_filtrado))

