import pandas as pd
import json


class DensityExtractor():
    def __init__(self, data_path: str):
        self._path_to_csv_data = data_path

    def get_csv_data(self) -> pd.DataFrame:
        csv_data = pd.read_csv(self._path_to_csv_data)
        csv_data = csv_data.rename(
            columns={
                "X": "longitude",
                "Y": "latitude",
                "Z": "population_density_km2"
            }
        )
        return csv_data

    def get_density_from_xy(self, longitude: float, latitude: float)-> pd.DataFrame:
        csv_data = self.get_csv_data(self._path_to_csv_data)
        csv_data[csv_data[longitude] == longitude]



if (__name__ == '__main__'):
    directory_density_path = f"config\cfg_density_population.json"

    with open(directory_density_path) as f:
        data_json = json.load(f)

    # Print the data (it will be stored as a Python dictionary)
    density_population_path = data_json['path_csv']

    dens_extractor = DensityExtractor(density_population_path)
    df = dens_extractor.get_csv_data()
    print(df)
