from langchain_core.tools import tool, StructuredTool
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from sqlalchemy.engine import connection_memoize

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


from src.settings import connect_to_db
def query_tecniche(tecnica: str):
    connection = connect_to_db()
    query = """
SELECT *
FROM TECNICHE
WHERE tipo LIKE CONCAT('%%', %s, '%%')
   OR descrizione LIKE CONCAT('%%', %s, '%%')
ORDER BY
    LENGTH(tipo) - LENGTH(REPLACE(tipo, %s, '')) DESC,
    LENGTH(descrizione) - LENGTH(REPLACE(descrizione, %s, '')) DESC
LIMIT 1;
"""
    with connection.cursor() as cursor:
        # Execute the query with the parameter passed as a tuple
        cursor.execute(query, (tecnica, tecnica, tecnica, tecnica))
        result = cursor.fetchone()
    connection.close()
    return result

def query_piatto_from_tecnica(tecnica_id: int):
    connection = connect_to_db()
    query = """
SELECT P.nome, P.id
FROM PIATTI_TECNICHE
LEFT JOIN PIATTI AS P ON PIATTI_TECNICHE.id_piatto = P.id
WHERE id_tecnica = %s
LIMIT 1;
"""
    with connection.cursor() as cursor:
        cursor.execute(query, (tecnica_id,))
        result = cursor.fetchall()
    connection.close()
    return result[0]["id"]

print(query_piatto_from_tecnica(query_tecniche("Marinatura temp")["id"]))