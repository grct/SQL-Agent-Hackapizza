import os
from langchain_ibm import ChatWatsonx
import pymysql

parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 3000,
    "temperature": 0
}

llm = ChatWatsonx(
    model_id=os.environ["MODEL"],
    project_id=os.environ["PROJECT_ID"],
    params=parameters
)




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