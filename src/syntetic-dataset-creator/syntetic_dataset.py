import os
from dotenv import load_dotenv
from openai import OpenAI


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
    

class SynteticDataset:
    def __init__(self,
                 system_prompt: str,
                 folder_path: str):
        self.system_prompt = system_prompt
        self.folder_path = folder_path

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
                    "content": f"Please generate a synthetic dataset for the country: {country}."
                },
            ],
            timeout=300
        )
        message = response.choices[0].message.content
        return message
    
    def save_response_to_file(self, country: str, model: str = "deepseek/deepseek-r1"):
        response_llm = self.generate_response_llm(country)
        file_path = os.path.join(self.folder_path, "response_for_syntetic_dataset.txt")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # Crea la cartella se non esiste
        with open(file_path, "w") as file:
            file.write(response_llm)



if __name__ == '__main__':
    country = 'Rwanda'
    system_prompt = read_file("src\\prompt\\broadband_syntetic.txt")
    folder_path = "data"
    syntetic_broadband_dataset = SynteticDataset(system_prompt, folder_path)
    syntetic_broadband_dataset.save_response_to_file(country, model="deepseek/deepseek-r1")
