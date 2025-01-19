from langchain_core.tools import tool, StructuredTool
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from sqlalchemy.engine import connection_memoize

from src.semaphore import sem
from src.settings import llm, connect_to_db, vn


#@tool
def tool_ingredienti(ingrediente: str):
    """Chiama questo tool per cercare dei piatti che contengono un ingrediente specifico.

    Args:
        ingrediente: Il nome dell' ingrediente
    """

    sem.acquire()
    result = vn.ask(f"Trova i Piatti che utilizzano l'ingrediente {ingrediente}")
    sem.release()

    return result
