import pandas as pd
from haversine import haversine


class DensityExtractor():
    def __init__(self, data_path: str):
        self._path_to_csv_data = data_path

    @property
    def csv_data(self):
        return self._csv_data

    def load_csv_data(self) -> pd.DataFrame:
        csv_data = pd.read_csv(self._path_to_csv_data)
        csv_data = csv_data.rename(
            columns=
            {
                'X': 'longitude',
                'Y': 'latitude',
                'Z': 'population_density_km2'
            }
        )
        self._csv_data = csv_data

    def get_min_distance_density(self, latitude: float, longitude: float) -> float:
        coord_input = (latitude, longitude)
        dataset = self._csv_data

        dataset['distance_km'] = dataset.apply(
            lambda row: haversine(coord_input, (row['latitude'], row['longitude'])),
            axis=1
        )

        min_index = dataset['distance_km'].idxmin()
        # nearest_point = dataset.iloc[[min_index]] # this line if you want return a dataframe

        nearest_point = dataset.iloc[min_index]

        return nearest_point['distance_km']


# if (__name__ == '__main__'):
#     directory_density_path = "config\cfg_density_population.json"    

#     with open(directory_density_path) as f:
#         data_json = json.load(f)

#     # Print the data (it will be stored as a Python dictionary)
#     density_population_path = data_json['path_csv']

#     dens_extractor = DensityExtractor(density_population_path)
#     dens_extractor.load_csv_data()

#     latitude = -2.253439903
#     longitude = 30.80427933

#     density = dens_extractor.get_min_distance_density(latitude=latitude, longitude=longitude)
#     print(density)
