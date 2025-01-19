from pprint import pprint
from typing import TypedDict, Annotated, Dict, List

from langchain_core.messages import ToolMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field

from src.models import State
from src.settings import llm

def splitter(state: State):

    query = state["messages"][0]

    prompt = PromptTemplate(
        input_variables=["query"],
        template = """
        Il tuo compito è quello di dividere una richiesta in parti più piccole.
        Le domande che vengono poste hanno sempre l'obiettivo di trovare determinati piatti.
        
        Per esempio:
        Quali piatti includono gli Spaghi del Sole e sono preparati utilizzando almeno una tecnica di Surgelamento del di Sirius Cosmo?
        
        Devi essere in grado di capire che Gli Spaghi del Sole sono un ingrediente, mentre Surgelamento del di Sirius Cosmo è una tecnica per preparare dei piatti.
        Una volta diviso il compito in task più piccole, dovrai dare i compiti ai nodi con a disposizione i tools.
        
        Per darti un'idea, i tools disponibili riguardano le singole metriche, come: Tecniche, Ingredienti e Licenze
        
        Domanda dell'utente:
        {query}
""")

    chain = prompt | llm
    return {"messages": chain.invoke(input={"query": query})}


