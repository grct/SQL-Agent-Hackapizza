from langchain_core.tools import tool, StructuredTool
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from sqlalchemy.engine import connection_memoize

from src.settings import llm, connect_to_db


#@tool
def tool_tecniche(tecnica: str):
    """Chiama questo tool quando l'utente chiede dei piatti che rispettino le quantità legali prescritte dal Codice di Galattico.

    Args:

    """

    # todo mettere vanna
