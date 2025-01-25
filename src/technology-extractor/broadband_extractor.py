import pandas as pd

from utils import get_offset_in_degrees, haversine_vectorized


class BroadbandExtractor:
    def __init__(self,
                 dataset_path: str
                 ):
        self.dataset_path = dataset_path
        self.data = self.read_data()
    
    def read_data(self):
        df = pd.read_csv(self.dataset_path)
        return df
    
    def get_broadband_availability(self, latitude: float, longitude: float, tolerance: float = 1.0):
        lat_offset, lon_offset = get_offset_in_degrees(latitude, tolerance)

        # Definisci i limiti di latitudine e longitudine in base all'offset
        lat_min = latitude - lat_offset
        lat_max = latitude + lat_offset
        lon_min = longitude - lon_offset
        lon_max = longitude + lon_offset

        # Filtra il DataFrame in base ai limiti
        mask_bool = (self.data['Latitude'] >= lat_min) & (self.data['Latitude'] <= lat_max) & (self.data['Longitude'] >= lon_min) & (self.data['Longitude'] <= lon_max)
        filtered_data = self.data[mask_bool]

        # Calcolare la distanza solo per i dati filtrati
        distances = haversine_vectorized(filtered_data['Latitude'], filtered_data['Longitude'], latitude, longitude)
        # Filtra ulteriormente in base alla tolleranza della distanza
        available_connections = filtered_data[distances <= tolerance]
        if (len(available_connections) >= 1):
            return True
        return False
    
    
# if __name__ == '__main__':
#     cellular_line_extractor = BroadbandExtractor('data\\rwanda_broadband_dataset.csv')
#     data = cellular_line_extractor.get_broadband_availability(latitude=-1.88, longitude=29.558)
#     print(data)

