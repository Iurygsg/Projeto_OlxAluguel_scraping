
import pandas as pd
import re

caminho = r'Projeto_OlxAluguel_scraping/dados/dados_olx_completo.xlsx'  
df=pd.read_excel(caminho) #lendo original



    
def exportar_dados(df,caminho):
    df["Valor"] = df["Valor"].apply(lambda x : re.sub(r'[^\d,]', '', x).replace(',','.'))
    df["Valor"] = pd.to_numeric(df["Valor"], errors='coerce')
    df["Valor"] = df["Valor"].astype(float)

    df.to_excel(caminho, index=True)
    print('dados exportados')


teste = exportar_dados(df,caminho)