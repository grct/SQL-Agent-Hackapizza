from langchain_core.tools import tool, StructuredTool
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore

from src.settings import llm


@tool
async def tool_tecniche(tecnica: str):
    """Chiama questo tool per cercare dei piatti solo quando richiedono una specifica tecnica data in input.

    Args:
        tecnica: Il nome della tecnica
    """

    system = (
        f"Create a new Lang Graph tool that {query} using the following template."
        f"Replace the parts in caps with the code needed to make the tool work."
    )

    context = f"""
    """
    code = llm.invoke([("system", system), ("human", context)])


    return {"messages": f"New tool {name} created"}