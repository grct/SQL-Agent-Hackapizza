import os
from langchain_ibm import WatsonxLLM

###TEST CONNESSIONE
watsonx_llm = WatsonxLLM(
    model_id=os.environ["MODEL"],
    project_id=os.environ["PROJECT_ID"],
)
print(watsonx_llm.invoke("Perchè Datapizza è la community più figa d'Italia?"))

