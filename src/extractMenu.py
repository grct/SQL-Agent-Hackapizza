import os
import json
from typing import Dict, List
from langchain_ibm import WatsonxLLM
from langchain.document_loaders import PyPDFLoader
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from pathlib import Path


class Dish(BaseModel):
    name: str = Field(description="Nome del piatto")
    ingredients: List[str] = Field(description="Lista degli ingredienti del piatto")
    techniques: List[str] = Field(description="Lista delle tecniche di preparazione")

class Restaurant(BaseModel):
    name: str = Field(description="Nome del ristorante")
    chef: str = Field(description="Nome dello Chef")
    skill: List[Dict[str, str]] = Field(description="Lista di Certificazioni o Skill con nome e livello")

class MenuResponse(BaseModel):
    piatti: List[Dish] = Field(description="Lista dei piatti nel menu")
    ristorante: Restaurant = Field(description="Ristorante del menu")


class MenuProcessor:
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

        # Set up the parser with our Pydantic model
        self.parser = JsonOutputParser(pydantic_object=MenuResponse)

        # Create prompt template with parser instructions
        self.extract_prompt = PromptTemplate(
            template="""
                Analizza il menu per recuperare le informazioni sul ristorante:
                - Il nome del ristorante
                - Il nome della chef
                - La lista di Skill e Certificazioni con il proprio livello
                
                Il livello delle Skill può essere anche in numero romano quindi convertilo.
                
                
                Analizza i piatti del menù per recuperare queste informazioni:
                - Il nome del piatto
                - La lista degli ingredienti sotto la sezione "Ingredienti"
                - La lista delle tecniche sotto la sezione "Tecniche"

                {format_instructions}

                Menu:
                {text}
            """,
            input_variables=["text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def save_to_json(self, menu_name: str, data: MenuResponse):
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

    def process_pdf(self, pdf_path: str) -> MenuResponse:
        """
        Processa un singolo file PDF e restituisce la lista dei piatti.
        """
        # Carica il PDF
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        # Unisci il testo di tutte le pagine
        text = " ".join([page.page_content for page in pages])

        # Create and execute the chain with the parser
        chain = self.extract_prompt | self.llm | self.parser

        try:
            result = chain.invoke({"text": text})
            menu_response = MenuResponse(**result)
            return menu_response
        except Exception as e:
            print(f"Errore nell'elaborazione del menu {pdf_path}: {str(e)}")
            return MenuResponse(piatti=[])

    def process_directory(self, directory_path: str) -> Dict[str, MenuResponse]:
        """
        Processa tutti i PDF in una directory e salva i risultati in file JSON.
        """
        results = {}
        path = Path(directory_path)

        for pdf_file in path.glob("*.pdf"):
            try:
                menu_response = self.process_pdf(str(pdf_file))
                results[pdf_file.name] = menu_response

                # Salva i risultati in un file JSON
                self.save_to_json(pdf_file.name, menu_response)

            except Exception as e:
                print(f"Errore nel processare {pdf_file}: {str(e)}")
                continue

        return results


if __name__ == "__main__":
    processor = MenuProcessor()
    results = processor.process_directory("../docs/menu/")

    # Stampa un riepilogo dei risultati
    for pdf_name, menu_response in results.items():
        print(f"\nMenu: {pdf_name}")
        print(f"Numero di piatti estratti: {len(menu_response.piatti)}")