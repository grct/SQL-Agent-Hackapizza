import os
from langchain_ibm import ChatWatsonx
import pymysql
from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore

parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 3000,
    "temperature": 0
}

llm = ChatWatsonx(
    model_id="mistralai/mistral-large",
    project_id=os.environ["PROJECT_ID"],
    params=parameters
)


class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None, allow_llm_to_see_data=True):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)



vn = MyVanna(config={'api_key': os.getenv('OPENAI_API_KEY'), 'model': 'gpt-4o-mini', 'temperature':0})


# Connessione al database MySQL
def connect_to_db():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )