from typing import TypedDict, Annotated, Dict

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool, StructuredTool
from pydantic import BaseModel, Field

from src.settings import llm

class Evaluation(BaseModel):
    evaluation: float = Field(description="float evaluation between 0 and 1")

class Risultato(BaseModel):
    query: str = Field(description="Domanda dell'utente")
    generated: str = Field(description="Dato generato da LLM")


def tool_evaluator(risultato: Risultato):
    """Chiama questo tool per verificare la correttezza di un dato generato.

    Args:
        risultato: Risultato ottenuto da un tool
    """

    prompt = PromptTemplate(
        input_variables=["query", "generated"],
        template = f"""
Devi valutare un dato rispetto a una domanda principale, calcolando un punteggio complessivo da 0 a 1 in base a quanto il dato sia inerente alla domanda.

Restituisci solo un punteggio numerico da 0 a 1, calcolato sulla base dei criteri sopra indicati.

1. Esempio di input:
Domanda principale: "Quali piatti offrono i ristoranti vicino a casa di Mario offrono piatti vegani?"
Dato ricevuto: "Ristorante A - Distanza: 500 m"

1. Output atteso:
Punteggio: 0.86

2. Esempio di input:
Domanda principale: "Che piatti ha il ristorante di Mario?"
Dato ricevuto: "Ristorante di Mario"

2. Output atteso:
Punteggio: 1.00


DOMANDA:
{risultato.query}

DATO DA VALUTARE:
{risultato.generated}
""")

    parser = JsonOutputParser(pydantic_object=Evaluation)
    chain = prompt | llm | parser
    ev = chain.invoke({"query": risultato.query, "generated": risultato.generated})

    return ev