import pandas as pd

from utils import get_offset_in_degrees, haversine_vectorized


class CellularLineExtractor:
    def __init__(self,
                 dataset_path: str
                 ):
        self.dataset_path = dataset_path
        self.data = self.read_data()
    
    def read_data(self):
        df = pd.read_csv(self.dataset_path)
        return df

    def get_cellular_line_availability(self, latitude: float, longitude: float, tolerance: float = 1.0):
        lat_offset, lon_offset = get_offset_in_degrees(latitude, tolerance)

        # Definisci i limiti di latitudine e longitudine in base all'offset
        lat_min = latitude - lat_offset
        lat_max = latitude + lat_offset
        lon_min = longitude - lon_offset
        lon_max = longitude + lon_offset

        # Filtra il DataFrame in base ai limiti
        mask_bool = (self.data['lat'] >= lat_min) & (self.data['lat'] <= lat_max) & (self.data['lon'] >= lon_min) & (self.data['lon'] <= lon_max)
        filtered_data = self.data[mask_bool]

        # Calcolare la distanza solo per i dati filtrati
        distances = haversine_vectorized(filtered_data['lat'], filtered_data['lon'], latitude, longitude)
        # Filtra ulteriormente in base alla tolleranza della distanza
        available_connections = filtered_data[distances <= tolerance]
        if (len(available_connections) >= 1):
            return True
        return False
    

# if __name__ == '__main__':
#     cellular_line_extractor = CellularLineExtractor('data\\rwanda_cellular_line.csv')
#     data = cellular_line_extractor.get_cellular_line_availability(latitude=-2.220000029, longitude=30.75839043)
#     print(data)
