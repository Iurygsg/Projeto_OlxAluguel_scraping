# testegeo.py

#Validar o metodo geopy pra medir as distancias

from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time
import pandas as pd

df=pd.read_excel(r"dados/dados_olx_valid.xlsx")

def separar_cidade_bairro(df):
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

dftratado=separar_cidade_bairro(df)
dftratado.head()