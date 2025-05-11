#classificação dos dados

import pandas as pd
import numpy as np


class ClassificacaoAHP:
    def __init__(self, df, caminho):
        self.df = df
        self.n = len(df)
        self.caminho = caminho

    def matriz_preferencia_preco(self):
        precos = self.df["Valor"].values
        matriz = np.ones((self.n, self.n))
        dif_max = np.max(np.abs(precos[:, None] - precos[None, :]))

        for i in range(self.n):
            for j in range(i + 1, self.n):
                dif = abs(precos[i] - precos[j])
                nota = 1 if dif_max == 0 else 1 + 8 * (dif / dif_max)
                matriz[i, j] = nota
                matriz[j, i] = 1 / nota
                
        matriz_preco = matriz / matriz.sum(axis=0)  #matriz normalizada Passo 2
        vetormedia_preco = matriz_preco.sum(axis=1) / len(matriz_preco) # média de cada linha

        print("Coluna media preço \n",  vetormedia_preco)

        return vetormedia_preco

    def matriz_preferencia_distancia(self):
        distancias = self.df["Distância do Ref (km)"].values
        matriz = np.ones((self.n, self.n))
        dif_max = np.max(np.abs(distancias[:, None] - distancias[None, :]))

        for i in range(self.n):
            for j in range(i + 1, self.n):
                dif = abs(distancias[i] - distancias[j])
                nota = 1 if dif_max == 0 else 1 + 8 * (1 - (dif / dif_max))
                matriz[i, j] = nota
                matriz[j, i] = 1 / nota

        matriz_distancia = matriz / matriz.sum(axis=0) # matriz normalizada Passo 2
        vetormedia_distancia = matriz_distancia.sum(axis=1) / len(matriz_distancia) # média de cada linha

        print("Coluna media distancia \n",  vetormedia_distancia)

        return vetormedia_distancia
    
    def matriz_pesocriterios(self):
        matriz = np.array([
            [1, 5],
            [1/5, 1]
        ])
        matriz = matriz / matriz.sum(axis=0)
        matriz = matriz.sum(axis=1) / len(matriz)
        print("vetor pesos \n",  matriz)
        return matriz
    
    def pontuacao_final(self):
        vetor_preco = self.matriz_preferencia_preco()
        vetor_dist = self.matriz_preferencia_distancia()
        vetor_criterio = self.matriz_pesocriterios()
        
        matriz_prioridades = np.vstack([vetor_preco, vetor_dist]).T  # n x 2
        vetor_resultado = matriz_prioridades @ vetor_criterio         # n x 1
        self.df["Pontuação Preço"] = vetor_preco
        self.df["Pontuação Distância"] = vetor_dist
        self.df["Pontuação Final"] = vetor_resultado
        self.df.to_excel(self.caminho, index=True)
        return self.df
    

