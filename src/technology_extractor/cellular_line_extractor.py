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
    
    def parse_dataset_format(self, available_connections: pd.DataFrame, distances: pd.Series, id_school: str, name_school: str, latitude_school: float, longitude_school: float) -> pd.DataFrame:
        available_connections['id_school'] = id_school
        available_connections['name_school'] = name_school
        available_connections['type_technology'] = 'cellular_tower'
        available_connections['latitude_school'] = latitude_school
        available_connections['longitude_school'] = longitude_school
        available_connections['distance_km_school_service_point'] = distances
        available_connections = available_connections.rename(columns={"lat": "latitude_service_point", 'lon': 'longitude_service_point', 'range': 'tower_range_meters'})
        important_columns = ['id_school', 'name_school', 'latitude_school', 'longitude_school', 'type_technology', 'latitude_service_point', 'longitude_service_point', 'tower_range_meters', 'distance_km_school_service_point']
        available_connections = available_connections[important_columns]
        return available_connections


    def get_cellular_line_availability(self, id_school: str, name_school: str, latitude_school: float, longitude_school: float, tolerance: float = 10.0, extract_only_top_5: bool = True):
        lat_offset, lon_offset = get_offset_in_degrees(latitude_school, tolerance)

        # Definisci i limiti di latitudine e longitudine in base all'offset
        lat_min = latitude_school - lat_offset
        lat_max = latitude_school + lat_offset
        lon_min = longitude_school - lon_offset
        lon_max = longitude_school + lon_offset

        # Filtra il DataFrame in base ai limiti
        mask_bool = (self.data['lat'] >= lat_min) & (self.data['lat'] <= lat_max) & (self.data['lon'] >= lon_min) & (self.data['lon'] <= lon_max)
        filtered_data = self.data[mask_bool]

        # Calcolare la distanza solo per i dati filtrati
        distances = haversine_vectorized(filtered_data['lat'], filtered_data['lon'], latitude_school, longitude_school)
        # Filtra ulteriormente in base alla tolleranza della distanza
        available_connections = filtered_data[distances <= tolerance]

        available_connections = self.parse_dataset_format(available_connections, distances, id_school, name_school, latitude_school, longitude_school)
        if extract_only_top_5:
            return available_connections.sort_values('distance_km_school_service_point').head(5)
        return available_connections

    

# if __name__ == '__main__':
#     list_locations = [{'lat': -1.88, 'lon': 29.5},
#                       {'lat': -1.78, 'lon': 31.5},
#                       {'lat': -1.98, 'lon': 28.5},
#                       {'lat': -1.765, 'lon': 27.5},
#                       {'lat': -1.68, 'lon': 31.5}]
#     cellular_line_extractor = CellularLineExtractor('data\\rwanda_cellular_line.csv')
#     for el in list_locations:
#         data = cellular_line_extractor.get_cellular_line_availability(id_school='id_prova', name_school='nome_prova', latitude_school=el['lat'], longitude_school=el['lon'])
#         print(data)
