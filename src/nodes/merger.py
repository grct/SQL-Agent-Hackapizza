from pprint import pprint
from typing import TypedDict, Annotated, Dict, List

from langchain_core.messages import ToolMessage
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


def merger(state: Dict):
    """Questo tool serve ad elaborare una risposta alla domanda dell'utente utilizzando i dati precedentemente generati.

    """


    x = [e.content for e in state.get("messages") if type(e) == ToolMessage]

    query = state["messages"][0]

    prompt = PromptTemplate(
        input_variables=["query", "x"],
        template = """
        Il tuo compito è quello di fornire i giusti ID dei piatti che l'utente richiede.
        L'utente ha fatto questa domanda: {query}
        
        Queste sono i piatti che sono stati trovati:
        {x}
        
        In base alla domanda dell'utente, tieni solo i piatti che ha chiesto e rispondimi con la lista in json.
        Rispondi solo con la lista json e nient'altro
""")

    chain = prompt | llm

    #return chain.invoke(input={"query": query, "x": x})
    return {"result": chain.invoke(input={"query": query, "x": x})}


