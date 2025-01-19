import os
import json
from typing import Dict, List, Optional
from langchain_ibm import WatsonxLLM
from langchain.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from pathlib import Path
import openai


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


class Tecniche(BaseModel):
    tipo: str = Field(description="Categoria di Tecnica")
    descrizione: str = Field(description="Nome della Tecnica")
    vantaggi: Optional[str] = Field(default="", description="Riassunto dei vantaggi")
    svantaggi: Optional[str] = Field(default="Svantaggi")  # Cambiato da str a Optional[str] con valore di default

class TecnicheList(BaseModel):
    tecnicheList: List[Tecniche] = Field(description="Lista Delle Tecniche di Preparazione")


openai.api_key = os.environ["OPENAI_API_KEY"]


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
        '''
        self.llm = WatsonxLLM(
            model_id=os.environ["MODEL"],
            project_id=os.environ["PROJECT_ID"],
            params=parameters
        )

        '''
        self.llm = ChatOpenAI(
            model_name="gpt-4o-2024-08-06",  # o altro modello a scelta
            temperature=0,
            max_tokens=3000,
            openai_api_key=os.environ["OPENAI_API_KEY"]
        )

        # Set up the parser with our Pydantic model
        self.parser = JsonOutputParser(pydantic_object=TecnicheList)

        # Create prompt template with parser instructions
        self.extract_prompt = PromptTemplate(
            template="""
                Estrai le tecniche e preparazioni recuperando le seguenti informazioni per ogni tecnica che trovi:
                - Categoria di Tecnica/Preparazione (ad esempio Marinatura)
                - Nome Categoria (ad esempio  Marinatura a Infusione Gravitazionale)
                - Vantaggi : riassunto corto dei vantaggi della tecnica
                - Svantaggi: riassunto corto degli svantaggi della tecnica
            
                
                {format_instructions}

                menu:
                {text}
            """,
            input_variables=["text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )

    def save_to_json(self, menu_name: str, data: TecnicheList):
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
        text = " ".join([page.page_content for page in pages[9:]])

        # Create and execute the chain with the parser
        chain = self.extract_prompt | self.llm | self.parser

        try:
            result = chain.invoke({"text": text})
            menu_response = TecnicheList(**result)
            return menu_response
        except Exception as e:
            print(f"Errore nell'elaborazione del menu {pdf_path}: {str(e)}")
            return ""

    def process_directory(self, directory_path: str) -> Dict[str, MenuResponse]:
        """
        Processa tutti i PDF in una directory e salva i risultati in file JSON.
        """
        results = {}
        path = Path(directory_path)

        for pdf_file in path.glob("*.pdf"):
            try:
                if not os.path.exists("../docs/json/"+ Path(str(pdf_file.name)).stem + ".json"):
                    print("Process file:  " + str(pdf_file.name))
                    menu_response = self.process_pdf(str(pdf_file))
                    results[pdf_file.name] = menu_response
                    print(menu_response)

                    # Salva i risultati in un file JSON
                    self.save_to_json(pdf_file.name, menu_response)

            except Exception as e:
                print(f"Errore nel processare {pdf_file}: {str(e)}")
                continue

        return results


if __name__ == "__main__":
    processor = MenuProcessor()
    results = processor.process_directory("../docs/")
