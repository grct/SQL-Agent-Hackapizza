from pprint import pprint
from typing import TypedDict, Annotated, Dict, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

from src.models import State
from src.settings import llm

class Piatti(BaseModel):
    p: List[int] = Field(description="list of integers")

class Inp(BaseModel):
    query: str
    piatti: List


def merger(state: Dict) -> List[int]:
    """Questo tool serve ad elaborare una risposta alla domanda dell'utente utilizzando i dati precedentemente generati.

    Args:
        input: Oggetto contenente la domanda iniziale dell'utente e la lista di piatti ottenuta dai tool precedentu
    """

    pprint(state)

    prompt = PromptTemplate(
        input_variables=["query", "generated"],
        template = f"""
Il tuo compito è quello di fornire una risposta adeguata alla domanda dell'utente con i dati a tua disposizione.

Domanda:
{state.get("query", "")}

Dati:
{[p for p in state.get("risultati", [])]}


""")

    print("STATE: ", state.get("messages")[-1].content)

    parser = JsonOutputParser(pydantic_object=Piatti)
    chain = prompt | llm | parser

