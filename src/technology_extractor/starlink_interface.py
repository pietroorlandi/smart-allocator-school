import pandas as pd
import json


class StarlinkInterface:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

    def _read_data(self):
        with open(self.dataset_path, 'r') as f:
            data = json.load(f)  # Dati già come oggetti Python (lista di dizionari)
            return data

    def get_starlink_avaiability(self, province: str, state: str) -> dict:
        data = self._read_data()  # Qui abbiamo già i dati come lista di dizionari, non serve json.loads

        # Crea un DataFrame da JSON
        df = pd.DataFrame(data)

        # Esegui una ricerca per provincia (ad esempio, "Lusaka")
        result = df[df['region'] == province]
        print(result)
        return result


# if __name__ == '__main__':
#     starlink_interface = StarlinkInterface('data\\starlink_africa_state.json')
#     starlink_interface.get_starlink_avaiability(province='Lusaka', state='')
