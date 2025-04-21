# testegeo.py

#Validar o metodo geopy pra medir as distancias

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time
import pandas as pd
import re

df=pd.read_excel(r"Projeto_OlxAluguel_scraping/dados/dados_olx_valid.xlsx")
# tratardados.py

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time
import pandas as pd

class Tratamento:
    def __init__(self, df, valor_maximo):
        self.df = df
        self.valor_maximo = valor_maximo
        self.geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0")
        self.local_referencia = "Padre Eustáquio"

    def geocode_with_retry(self, endereco, tentativas=3):
        for i in range(tentativas):
            try:
                loc = self.geolocator.geocode(endereco, timeout=10)
                return loc
            except Exception as e:
                print(f"Tentativa {i+1} falhou: {e}. Tentando novamente...")
                time.sleep(2)
        return None

    def separar_cidade_bairro(self):
        cidades = []
        bairros = []
        for local in self.df["Localizacao"]:
            partes = str(local).split(',')
            if len(partes) >= 2:
                cidade = partes[0].strip()
                bairro = ','.join(partes[1:]).strip()
            else:
                cidade = partes[0].strip()
                bairro = ''
            cidades.append(cidade)
            bairros.append(bairro)
        self.df["Cidade"] = cidades
        self.df["Bairro"] = bairros
        self.df.drop(columns=["Localizacao"], inplace=True)
    
    def remover_coluna(self):
       self.df["Valor"] = self.df["Valor"].astype(float)
       self.df["Valor"] = self.df["Valor"].apply(lambda x : re.sub(r'[^\d,]', '', x).replace(',','.'))
       self.df["Valor"] = pd.to_numeric(self.df["Valor"], errors='coerce')

    def calcular_distancia(self):
        print("Procurando coordenadas de referência...")
        ref = self.geocode_with_retry(self.local_referencia)
        if not ref:
            print("Erro ao geocodificar a referência. Encerrando.")
            return

        ref_coords = (ref.latitude, ref.longitude)
        distancias = []

        for cidade, bairro in zip(self.df["Cidade"], self.df["Bairro"]):
            endereco = f"{bairro}, {cidade}"
            loc = self.geocode_with_retry(endereco)
            if loc:
                anuncio_coords = (loc.latitude, loc.longitude)
                distancia_km = geodesic(ref_coords, anuncio_coords).km
                print(distancia_km)
            else:
                distancia_km = None
            distancias.append(distancia_km)

        self.df["Distância do Ref (km)"] = distancias
        print("Coluna de distâncias adicionada.")

    def processar(self):
        print("Iniciando processamento...")
        self.separar_cidade_bairro()
        self.calcular_distancia()
        print("Processamento finalizado.")
        return self.df
        
print("fim tratamento")

valor_maximo=2500
# Aplicar tratamento
tratar = Tratamento(df, valor_maximo)
df_tratado = tratar.processar()

# Salvar o resultado
df_tratado.to_excel("Projeto_OlxAluguel_scraping/dados/anuncios_tratado.xlsx", index=False)