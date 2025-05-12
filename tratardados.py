# tratardados.py

from geopy.geocoders import Nominatim
from geopy.distance import distance
import time
import winsound


class Tratamento:
    def __init__(self, df, valor_maximo, caminho):
        self.df = df.copy()
        self.valor_maximo = valor_maximo
        self.geolocator = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:137.0) Gecko/20100101 Firefox/137.0")
        self.local_referencia = "Belo Horizonte, Padre Eustáquio"
        self.caminho = caminho

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
        self.df[["Cidade", "Bairro"]] = self.df["Localizacao"].str.split(",", n=1, expand=True)
        self.df["Cidade"] = self.df["Cidade"].str.strip()
        self.df["Bairro"] = self.df["Bairro"].str.strip()
    
    def filtroValor(self):
       self.df = self.df[self.df["Valor"] <= self.valor_maximo].copy()
       self.df = self.df[self.df["Valor"] != "N/D"].copy()

    def calcular_distancia(self):
        print("Procurando coordenadas de referência...")
        ref = self.geocode_with_retry(self.local_referencia)
        print("local de ref: ", ref)
        if not ref:
            print("Erro ao geocodificar a referência. Encerrando.")
            return

        ref_coords = (ref.latitude, ref.longitude)
        print("local de ref: ", ref_coords)
        distancias = []

        for cidade, bairro in zip(self.df["Cidade"], self.df["Bairro"]):
            endereco = f"{bairro}, {cidade}"
            loc = self.geocode_with_retry(endereco)
            if loc:
                anuncio_coords = (loc.latitude, loc.longitude)
                distancia_km = distance(ref_coords, anuncio_coords).km
                print("diferenca dist:", distancia_km)
            else:
                distancia_km = None
            distancias.append(distancia_km)

        self.df.loc[:, "Distância do Ref (km)"] = distancias
        self.df.dropna(subset=["Distância do Ref (km)"], inplace = True)
        print("Coluna de distâncias adicionada.")

    def processar(self):
        print("Iniciando processamento...")
        self.separar_cidade_bairro()
        self.filtroValor()
        self.calcular_distancia()
        self.df.to_excel(self.caminho, index=False)
        print("Processamento finalizado.")
        winsound.MessageBeep()
        return self.df

