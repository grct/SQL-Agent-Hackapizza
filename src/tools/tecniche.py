from typing import Annotated

from langchain_core.messages import ToolMessage
from langchain_core.tools import tool, StructuredTool, InjectedToolCallId
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from langgraph.prebuilt import InjectedState
from sqlalchemy.engine import connection_memoize
from langgraph.types import Command

from src.semaphore import fun, sem

from src.models import State
from src.settings import llm, connect_to_db, vn


class ToolResult:
    pass


@tool
def tool_tecniche(tecnica: str, state: Annotated[dict, InjectedState]):
    """Chiama questo tool per cercare dei piatti solo quando richiedono una specifica tecnica data in input.

    Args:
        tecnica: Il nome della tecnica
    """

    sem.acquire()
    res = vn.ask(f"Trova i Piatti che utilizzano la Tecnica {tecnica}")
    sem.release()


    return res[1]
