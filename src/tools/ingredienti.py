from langchain_core.tools import tool, StructuredTool
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore, VectorStore
from sqlalchemy.engine import connection_memoize

from src.settings import llm, connect_to_db


#@tool
def tool_tecniche(ingrediente: str):
    """Chiama questo tool per cercare dei piatti che contengono un ingrediente specifico.

    Args:
        ingrediente: Il nome dell' ingrediente
    """

    connection = connect_to_db()

    query = """
SELECT P.nome, P.id
FROM PIATTI_INGREDIENTI PT
JOIN (
    SELECT *
    FROM INGREDIENTI
    WHERE nome LIKE CONCAT('%%', %(ingrediente)s, '%%')
    ORDER BY
        LENGTH(nome) - LENGTH(REPLACE(nome, %(ingrediente)s, '')) DESC
    LIMIT 1
) TS ON PT.id_ingrediente = TS.id
LEFT JOIN PIATTI AS P ON PT.id_piatto = P.id;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, {'ingrediente': ingrediente})
        result = cursor.fetchall()
    connection.close()
    return [r["id"] for r in result]