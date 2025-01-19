
from langchain_core.tools import tool

from src.nodes.merger import Inp
from src.semaphore import sem
from src.settings import vn


class ToolResult:
    pass


@tool
def tool_tecniche(tecnica: str):
    """Chiama questo tool per cercare dei piatti solo quando richiedono una specifica tecnica data in input.
    Un piatto può avere più tecniche.

    Args:
        tecnica: Il nome della tecnica
    """

    sem.acquire()
    result = vn.ask(f"Trova i Piatti che utilizzano la Tecnica {tecnica}", visualize=False)
    sem.release()

    if len(result):
        return Inp(
            query=f"Piatti con la tecnica: {tecnica}",
            piatti=[e[0] for e in result[1].values]
        )
    else:
        return Inp(
            query=f"Piatti con la tecnica: {tecnica}",
            piatti=[]
        )