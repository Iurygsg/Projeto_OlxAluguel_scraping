from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class Tratamento:
    def __init__(self, df):
        self.df = df
        print(df)
        return df
    # Inicializa o geolocalizador
    geolocator = Nominatim(user_agent="App_busca")

    # Coordenadas de referência do bairro Padre Eustáquio, BH
    local_referencia = "Padre Eustáquio, Belo Horizonte, MG"
    local_ref_coords = geolocator.geocode(local_referencia)
    

    