#classificação dos dados

import pandas as pd
import numpy as np
import re
df=pd.read_excel(r"Projeto_OlxAluguel_scraping/dados/dados_olx_valid.xlsx")
class ClassificacaoAHP:
    def __init__(self, df):
        self.df = df

    def matriz_preferencia_preco(self):
        # self.df["Valor"] = self.df["Valor"].apply(lambda x : re.sub(r'[^\d,]', '', x).replace(',','.'))
        # self.df["Valor"] = self.df["Valor"].astype(float)
        # self.df["Valor"] = pd.to_numeric(self.df["Valor"], errors='coerce')
        precos = self.df["Valor"].values
        n = len(precos)

        matriz = np.ones((n, n))
        
        dif_max = np.max(np.abs(precos[:, None] - precos[None, :]))

        for i in range(n):
            for j in range(i + 1, n):
                dif = abs(precos[i] - precos[j])
                nota = 1 if dif_max == 0 else 1 + 8 * (dif / dif_max)
                matriz[i, j] = nota
                matriz[j, i] = 1 / nota

        df_matriz = pd.DataFrame(matriz, index=self.df.index, columns=self.df.index)
        return df_matriz
    
    def matriz_preferencia_distancia(self):
        distancias = self.df["Distância do Ref (km)"].values
        n = len(distancias)

        matriz = np.ones((n, n))
        dif_max = np.max(np.abs(distancias[:, None] - distancias[None, :]))

        for i in range(n):
            for j in range(i + 1, n):
                dif = abs(distancias[i] - distancias[j])
                nota = 1 if dif_max == 0 else 1 + 8 * (1 - (dif / dif_max))
                matriz[i, j] = nota
                matriz[j, i] = 1 / nota

        df_matriz = pd.DataFrame(matriz, index=self.df.index, columns=self.df.index)
        return df_matriz
    
    # def classificar():
    #     matriz_preco = tratar.matriz_preferencia_preco()
    #     matriz_distancia = tratar.matriz_preferencia_distancia()
    #     return matriz_classificacao

tratar = ClassificacaoAHP(df)
matriz_preco = tratar.matriz_preferencia_preco()
matriz_distancia = tratar.matriz_preferencia_distancia()

print("M. Preço\n", matriz_preco)
print("M. Distancia\n", matriz_distancia)