from langchain_core.tools import tool

from src.nodes.merger import Inp
from src.semaphore import sem
from src.settings import vn


@tool
def tool_ingredienti(licenza: str, livello: int):
    """Chiama questo tool per cercare dei piatti cucinati da Chief o Ristoranti con delle determinate Licenze o Certificazioni.

    Args:
        licenza: Il nome della Licenza o Certificazione
        livello: Il livello della Licenza o Certificazione
    """

    query = f"Trova i Piatti dei Ristoranti che utilizzano la licenza {licenza} con il livello {livello}"

    sem.acquire()
    result = vn.ask(query)
    sem.release()

    if len(result):
        return Inp(
            query=f"Piatti con licenza: {licenza} di livello {livello}",
            piatti=[e[0] for e in result[1].values]
        )
    else:
        return Inp(
            query=f"Piatti con licenza: {licenza} di livello {livello}",
            piatti=[]
        )
