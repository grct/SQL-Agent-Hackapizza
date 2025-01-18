import os
import json
from typing import Dict, List
from langchain_ibm import WatsonxLLM
from langchain.agents import tool
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from pathlib import Path
from prompt import restaurant_prompt, dish_prompt, skill_prompt




class Dish(BaseModel):
    dishName: str = Field(description="Nome del piatto")
    ingredients: List[str] = Field(description="Lista degli ingredienti del piatto")
    techniques: List[str] = Field(description="Lista delle tecniche di preparazione")
class Restaurant(BaseModel):
    name: str = Field(description="Nome del ristorante")
    chef: str = Field(description="Nome dello Chef")
class Skill(BaseModel):
    skillName: str = Field(description="Nome della Skill/Certificazione")
    level: str = Field(description="Livello della Skill/Certificazione")

class TotalEntities(BaseModel):
    restaurantInfo: Restaurant
    skillList: List[Skill]
    dishList: List[Dish]

class MenuExtractor:
    def __init__(self):
        """
        Inizializza WatsonxLLM con i dettagli del modello e del progetto.
        """
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 3000,
            "temperature": 0
        }

        self.llm = WatsonxLLM(
            model_id=os.environ["MODEL"],
            project_id=os.environ["PROJECT_ID"],
            params=parameters
        )

    def processPdf(self, pdf_path: str, prompt: PromptTemplate, parser: JsonOutputParser):
        """
        Processa un singolo file PDF e restituisce la lista dei piatti.
        """
        # Carica il PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        # Unisci il testo di tutte le pagine
        text = " ".join([page.page_content for page in pages])

        # Create and execute the chain with the parser
        chain = prompt | self.llm | parser

        try:
            result = chain.invoke({"text": text})
            return result
        except Exception as e:
            print(f"Errore nell'elaborazione del menu {pdf_path}: {str(e)}")
            return ""

    def process_directory(self, directory_path: str):
        """
        Processa tutti i PDF in una directory e salva i risultati in file JSON.
        """
        results = {}
        path = Path(directory_path)

        for pdf_file in path.glob("*.pdf"):
            try:
                if not os.path.exists("../docs/json/"+ Path(str(pdf_file.name)).stem + ".json"):
                    print("Process file:  " + str(pdf_file.name))
                    '''restaurantParser = JsonOutputParser(pydantic_object=Restaurant)
                    promptRestaurant = PromptTemplate(
                            template=restaurant_prompt,
                            input_variables=["text"],
                            partial_variables={"format_instructions": restaurantParser.get_format_instructions()}
                        )
                    restaurantResponse = self.processPdf(str(pdf_file), promptRestaurant, restaurantParser)
                    print(restaurantResponse)

                    skillParser = JsonOutputParser(pydantic_object=Skill)
                    promptSkill = PromptTemplate(
                            template=skill_prompt,
                            input_variables=["text"],
                            partial_variables={"format_instructions": skillParser.get_format_instructions()}
                        )
                    skillResponse = self.processPdf(str(pdf_file), promptSkill, skillParser)
'''
                    dishParser = JsonOutputParser(pydantic_object=Dish)
                    promptDish = PromptTemplate(
                            template=dish_prompt,
                            input_variables=["text"],
                            partial_variables={"format_instructions": dishParser.get_format_instructions()}
                        )
                    dishResponse = self.processPdf(str(pdf_file), promptDish, dishParser)
                    print(dishResponse)
                    for dish in dishResponse:
                        print(dish)

                    dish_list = [Dish(**dish) for dish in dishResponse]
                    print(dish_list)
                    '''restaurant_obj = Restaurant(**restaurantResponse)
                    print(restaurant_obj)
                    skill_list = [Skill(**skill) for skill in skillResponse]
                    print(skill_list)
                    

                    # Crea il TotalEntities con gli oggetti creati
                    total_entities = TotalEntities(
                        restaurantInfo=restaurant_obj,
                        skillList=skill_list,
                        dishList=dish_list
                    

                    results = total_entities

                    self.save_to_json(pdf_file.name, total_entities))'''

            except Exception as e:
                print(f"Errore nel processare {pdf_file}: {str(e)}")
                continue

        return results

    def save_to_json(self, menu_name: str, data: TotalEntities):
        """
        Salva i risultati in un file JSON nella cartella 'json'.

        Args:
            menu_name (str): Nome del menu (nome del file PDF)
            data (MenuResponse): Dati da salvare
        """
        # Crea la cartella json se non esiste
        json_dir = Path("../docs/json")
        json_dir.mkdir(exist_ok=True)

        # Rimuovi l'estensione .pdf e aggiungi .json
        json_filename = Path(menu_name).stem + ".json"
        json_path = json_dir / json_filename

        # Converti i dati in formato JSON e salvali
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data.model_dump(), f, ensure_ascii=False, indent=2)

        print(f"Risultati salvati in: {json_path}")

if __name__ == "__main__":
    dish_data = {
        'dishName': 'Sinfonia Quantistica delle Stelle',
        'ingredients': [
            'Shard di Prisma Stellare', 'Lattuga Namecciana',
            'Radici di Singolarità Fibra di Sintetex', 'Carne di Balena spaziale',
            'Teste di Idra', 'Nettare di Sirena', 'Sale Temporale'
        ],
        'techniques': ['Marinatura Temporale Sincronizzata']
    }


    extractor = MenuExtractor()
    results = extractor.process_directory("../docs/menu/")