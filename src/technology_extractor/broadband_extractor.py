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

    def parse_dataset_format(self, available_connections: pd.DataFrame, distances: pd.Series, id_school: str, name_school: str, latitude_school: float, longitude_school: float) -> pd.DataFrame:
        available_connections['id_school'] = id_school
        available_connections['name_school'] = name_school
        available_connections['tower_range_meters'] = None
        available_connections['latitude_school'] = latitude_school
        available_connections['longitude_school'] = longitude_school
        available_connections['distance_km_school_service_point'] = distances
        available_connections = available_connections.rename(columns={"Latitude": "latitude_service_point", 'Longitude': 'longitude_service_point', 'Connection Type': 'type_technology'})
        important_columns = ['id_school', 'name_school', 'latitude_school', 'longitude_school', 'type_technology', 'latitude_service_point', 'longitude_service_point', 'tower_range_meters', 'distance_km_school_service_point']
        available_connections = available_connections[important_columns]
        return available_connections
    
    def get_broadband_availability(self, id_school: str, name_school: str, latitude_school: float, longitude_school: float, tolerance: float = 3.0, extract_only_top_5: bool = True) -> pd.DataFrame:
        lat_offset, lon_offset = get_offset_in_degrees(latitude_school, tolerance)

        # Definisci i limiti di latitudine e longitudine in base all'offset
        lat_min = latitude_school - lat_offset
        lat_max = latitude_school + lat_offset
        lon_min = longitude_school - lon_offset
        lon_max = longitude_school + lon_offset

        # Filtra il DataFrame in base ai limiti
        mask_bool = (self.data['Latitude'] >= lat_min) & (self.data['Latitude'] <= lat_max) & (self.data['Longitude'] >= lon_min) & (self.data['Longitude'] <= lon_max)
        filtered_data = self.data[mask_bool]

        # Calcolare la distanza solo per i dati filtrati
        distances = haversine_vectorized(filtered_data['Latitude'], filtered_data['Longitude'], latitude_school, longitude_school)
        # Filtra ulteriormente in base alla tolleranza della distanza
        available_connections = filtered_data[distances <= tolerance]
        available_connections['id_school'] = id_school
        available_connections['name_school'] = name_school
        available_connections['latitude_school'] = latitude_school
        available_connections['longitude_school'] = longitude_school
        available_connections['distance_km_school_broadband'] = distances
        available_connections = self.parse_dataset_format(available_connections, distances, id_school, name_school, latitude_school, longitude_school)
        if extract_only_top_5:
            return available_connections.sort_values('distance_km_school_service_point').head(5)

        return available_connections
    
if __name__ == '__main__':
    cellular_line_extractor = BroadbandExtractor('data\\rwanda_broadband_dataset.csv')
    data = cellular_line_extractor.get_broadband_availability(id_school='id_prova', name_school='nome_prova', latitude_school=-1.88, longitude_school=29.558)
    print(data)

