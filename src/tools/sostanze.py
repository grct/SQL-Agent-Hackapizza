from langchain_core.tools import tool, StructuredTool
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from sqlalchemy.engine import connection_memoize

from src.nodes.merger import Inp
from src.semaphore import sem
from src.settings import llm, connect_to_db, vn


#@tool
def tool_sostanza(sostanza: str):
    """
    Chiama questo tool per verificare le quantità di sostanza in un piatto.
    Questi sono i Limiti regolamentari
    CRP > 0.90: ≤ 0.5%; 0.65 ≤ CRP ≤ 0.90: ≤ 1%.
    IPM > 0.9: ≤ 4%.
    IBX > 0.7: ≤ 0.25%; μ > 0.5: ≤ 0.1%.
    δQ > 0.3: ≤ 3%.
    CDT > 0.7: ≤ 2%; CDT ≤ 0.7: ≤ 3%.

    Args:
        sostanza: Il nome della sostanza
    """

    sem.acquire()
    result = vn.ask(f"Trova i Piatti che utilizzano la Sostanza {sostanza}")
    sem.release()

    if len(result):
        return Inp(
            query=f"Piatti con la sostanza: {sostanza}",
            piatti=[e[0] for e in result[1].values]
        )
    else:
        return Inp(
            query=f"Piatti con la sostanza: {sostanza}",
            piatti=[]
        )