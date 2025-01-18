from langchain_core.tools import tool, StructuredTool
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from sqlalchemy.engine import connection_memoize

from src.settings import llm, connect_to_db


#@tool
def tool_tecniche(tecnica: str):
    """Chiama questo tool per cercare dei piatti solo quando richiedono una specifica tecnica data in input.

    Args:
        tecnica: Il nome della tecnica
    """

    connection = connect_to_db()

    query = """
    WITH tecnica_selezionata AS (
        SELECT *
        FROM TECNICHE
        WHERE tipo LIKE CONCAT('%%', %s, '%%')
           OR descrizione LIKE CONCAT('%%', %s, '%%')
        ORDER BY
            LENGTH(tipo) - LENGTH(REPLACE(tipo, %s, '')) DESC,
            LENGTH(descrizione) - LENGTH(REPLACE(descrizione, %s, '')) DESC
        LIMIT 1
    )
    SELECT P.nome, P.id
    FROM PIATTI_TECNICHE
    LEFT JOIN PIATTI AS P ON PIATTI_TECNICHE.id_piatto = P.id
    WHERE id_tecnica = (SELECT id FROM tecnica_selezionata);
    """

    with connection.cursor() as cursor:
        cursor.execute(query, tecnica)
        result = cursor.fetchall()
    connection.close()
    return [r["id"] for r in result]


print(tool_tecniche("Marinatura Temp"))