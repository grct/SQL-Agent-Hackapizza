import os
import json
import pymysql


def connect_to_db():
    return pymysql.connect(
        host="77.37.121.60",
        user="root",
        password="momentumdigital00",
        database="HackaPizza",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
def insert_data(json_data):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            # Query per inserire i dati
            query = """
                INSERT INTO TECNICHE (tipo, vantaggi, svantaggi, descrizione)
                VALUES (%s, %s, %s, %s)
            """

            for tecnica in json_data["tecnicheList"]:
                tipo = tecnica["tipo"]
                descrizione = tecnica["descrizione"]
                vantaggi = tecnica["vantaggi"]
                svantaggi = tecnica["svantaggi"]

                    # Eseguire la query di inserimento
                cursor.execute(query, (tipo, vantaggi, svantaggi, descrizione))

            # Salvare le modifiche
            connection.commit()

    except Exception as e:
        print(f"Errore durante l'inserimento dei dati: {e}")
        connection.rollback()

    finally:
        connection.close()


if __name__ == "__main__":
    with open('../docs/json/Manuale di Cucina_1.json', 'r', encoding='utf-8') as file:
      data = json.load(file)

    # Inserire i dati nel database
    insert_data(data)