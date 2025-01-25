class TechnologyExtractor:
    """
    Questo modulo si occupa di prendere le informazioni riguardanti le tecnologie disponibili in una determinata posizione (latitudine, longitudine) e ritornare un dizionario con le informazioni
    """
    def __init__(self,
                 config: dict):
        self.config = config
        self.dataset_broadband_path = self.config['dataset_broadband_path']
        self.dataset_cellular_line_path = self.config['dataset_cellular_line_path']
    
    def _is_starlink_avaiable(self, latitude: float, longitude: float):
        pass

    def get_technologies_avaiable(self, latitude: float, longitude: float):
        # 
        pass
