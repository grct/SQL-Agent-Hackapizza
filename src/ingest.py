import os

import requests
from langchain_ibm import WatsonxLLM

llm = WatsonxLLM(
    model_id=os.environ["MODEL"],
    project_id=os.environ["PROJECT_ID"],
)


# a = llm.invoke("QUanti giorni ci sono all'anno?")


from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(
    url=os.environ["WATSONX_URL"],
    api_key=os.environ["WATSONX_APIKEY"],
)

model = ModelInference(
    model_id="mistralai/mistral-large", # Che conosciamo bene 😊🏆
    credentials=credentials,
    project_id=os.environ["PROJECT_ID"],
    params={
        "max_tokens": 200
      }
)

result = model.chat(messages=[{'role': 'user', 'content': "Quale è la relazione tra lo spettro di un segnale e la trasformata di Fourier"}])

print(result['choices'][0]['message']['content'])

