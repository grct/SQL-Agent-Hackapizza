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
SELECT P.nome, P.id
FROM PIATTI_TECNICHE PT
JOIN (
    SELECT *
    FROM TECNICHE
    WHERE tipo LIKE CONCAT('%%', %(tecnica)s, '%%')
       OR descrizione LIKE CONCAT('%%', %(tecnica)s, '%%')
    ORDER BY
        LENGTH(tipo) - LENGTH(REPLACE(tipo, %(tecnica)s, '')) DESC,
        LENGTH(descrizione) - LENGTH(REPLACE(descrizione, %(tecnica)s, '')) DESC
    LIMIT 1
) TS ON PT.id_tecnica = TS.id
LEFT JOIN PIATTI AS P ON PT.id_piatto = P.id;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, {'tecnica': tecnica})
        result = cursor.fetchall()
    connection.close()

    if result:
        return [{
            "id": r["id"] for r in result
        }]
