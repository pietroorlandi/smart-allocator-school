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
    

class DocumentGenerator:
    def __init__(self,
                 system_prompt: str,
                 technology_data_path: str,
                 folder_path: str):
        self.system_prompt = system_prompt
        self.folder_path = folder_path
        self.technology_data_path = technology_data_path
        self.allocator_data = self._get_allocator_data()

    def _get_allocator_data(self):
        data = [{'school_id': 1,
            'technology': 'Broadband',
            'reason': "The closest cellular tower is 0.2157 km away with a range of 6928 meters. The estimated cost includes installation and maintenance.",
            'pop_density': 200,
            'isolation': 0.5,
            'cost': 600},
            {'school_id': 4,
            'technology': 'Cellular',
            'reason': "The closest cellular tower is 0.3541 km away with a range of 7571 meters. The estimated cost includes installation and maintenance.",
            'pop_density': 180,
            'isolation': 0.4,
            'cost': 100},
            {'school_id': 2,
            'technology': 'Broadband',
            'reason': "The closest broadband service point is 11.5951 km away. The estimated cost includes installation and maintenance for FTTH technology.",
            'pop_density': 150,
            'isolation': 0.3,
            'cost': 700},
            {'remaining_budget': 100}]
        return data

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
                    "content": f"""These are the data obtained from the allocator for the selected country: {country}.
                                    Data: {self.allocator_data}"""
                },
            ],
            timeout=300,
            max_tokens=20000
        )
        message = response.choices[0].message.content
        return message
    
    def save_response_to_file(self, country: str, model: str = "deepseek/deepseek-r1"):
        response_llm = self.generate_response_llm(country, model)
        print(f"Risposta LLM: {response_llm}")
        file_path = os.path.join(self.folder_path, "output_document.md")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Crea la cartella se non esiste
        with open(file_path, "w") as file:
            file.write(response_llm)



if __name__ == '__main__':
    country = 'Rwanda'
    system_prompt = read_file("src\\prompt\\document_creator.txt")
    folder_path = "report\\2025-01-26_13-34-02"
    technology_data_path = "report\\2025-01-26_14-48-56\\unconnected_schools_technology.csv"
    document_generator = DocumentGenerator(system_prompt, technology_data_path, folder_path)
    # model="mistralai/codestral-2501"
    document_generator.save_response_to_file(country, model="mistralai/codestral-2501")
