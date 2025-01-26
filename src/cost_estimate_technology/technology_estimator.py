import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

def read_file(file_path) -> str:
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Il file {file_path} non è stato trovato.")
        return None
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
        return None
    

class LLMEstimatorCost:
    def __init__(self,
                 system_prompt: str,
                 technology_data_path: str,
                 folder_path: str):
        self.system_prompt = system_prompt
        self.folder_path = folder_path
        self.technology_data_path = technology_data_path
        self.technology_data = self._get_technology_data()

    def _get_technology_data(self):
        return pd.read_csv(self.technology_data_path)

    def generate_response_llm(self, country: str, model: str = "deepseek/deepseek-r1"):
        load_dotenv()
        api_key = os.getenv("API_AI_KEY")
        client = OpenAI(
            base_url="https://api.aimlapi.com/v1",
            api_key=api_key,    
        )
        print(f"Sending request to LLM ({model})...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {
                    "role": "user",
                    "content": f"""Questi sono i dati CSV per il paese: {country}.
                                    Ecco i dati: {self.technology_data.to_csv()}"""
                },
            ],
            response_format={"type": "json_object"},
            timeout=300,
            max_tokens=10000
        )
        message = response.choices[0].message.content
        return message
    
    def save_response_to_file(self, country: str, model: str = "deepseek/deepseek-r1"):
        response_llm = self.generate_response_llm(country, model)
        print(f"Risposta LLM: {response_llm}")
        file_path = os.path.join(self.folder_path, "estimation_cost.json")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Crea la cartella se non esiste
        with open(file_path, "w") as file:
            file.write(response_llm)



if __name__ == '__main__':
    country = 'Rwanda'
    system_prompt = read_file("src\\prompt\\cost_estimator_system.txt")
    folder_path = "report\\2025-01-26_13-34-02"
    technology_data_path = "report\\2025-01-26_14-48-56\\unconnected_schools_technology.csv"
    syntetic_broadband_dataset = LLMEstimatorCost(system_prompt, technology_data_path, folder_path)
    # model="mistralai/codestral-2501"
    syntetic_broadband_dataset.save_response_to_file(country, model="mistralai/codestral-2501")
