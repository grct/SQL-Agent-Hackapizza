from langchain_core.tools import tool
from src.nodes.merger import Inp
from src.semaphore import sem
from src.settings import vn


@tool
def tool_ingredienti(ingrediente: str):
    """Chiama questo tool per cercare dei piatti che contengono un ingrediente specifico.

    Args:
        ingrediente: Il nome dell' ingrediente
    """

    query = f"Trova i Piatti che utilizzano l'ingrediente {ingrediente}"

    sem.acquire()
    result = vn.ask(query, visualize=False)
    sem.release()

    if len(result):
        return Inp(
            query=f"Piatti con ingrediente: {ingrediente}",
            piatti=[e[0] for e in result[1].values]
        )
    else:
        return Inp(
            query=f"Piatti con ingrediente: {ingrediente}",
            piatti=[]
        )
