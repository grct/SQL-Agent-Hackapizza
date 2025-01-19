from langchain_core.tools import tool
from src.nodes.merger import Inp
from src.semaphore import sem
from src.settings import vn
from src.settings import llm

@tool
def tool_distanza(distanza: str):
    """Chiama questo tool per avere informazioni sulle distanze

    Args:
        distanza: Richiesta sulla distanza
    """

    query = f"Trova i piatti che sono serviti in ristoranti che rispettano la condizione di distanza {distanza}"

    sem.acquire()
    result = vn.ask(query)
    print(result)
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


if __name__ == '__main__':
    print(tool_distanza("Trova i piatti che stanno a meno di 10 anni luce da Arrakis"))