import os
from langchain_ibm import WatsonxLLM

###TEST CONNESSIONE
watsonx_llm = WatsonxLLM(
    model_id=os.environ["MODEL"],
    project_id=os.environ["PROJECT_ID"],
)
print(watsonx_llm.invoke("Come sono relazionate le trasformate di fourier con lo spettro delle ampiezze?"))

