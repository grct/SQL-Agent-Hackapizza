import os
from langchain_ibm import WatsonxLLM

parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 3000,
    "temperature": 0
}

llm = WatsonxLLM(
    model_id=os.environ["MODEL"],
    project_id=os.environ["PROJECT_ID"],
    params=parameters
)


