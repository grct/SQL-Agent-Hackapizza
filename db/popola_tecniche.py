import pymysql
import json
import uuid
import os


# Connessione al database MySQL
def connect_to_db():
    return pymysql.connect(
        host=os.environ["DB_HOST"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"],
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

            for tecnica in json_data["tecniche"]:
                tipo = tecnica["nome"]
                for sotto_categoria in tecnica["sotto_categorie"]:
                    descrizione = sotto_categoria["nome"]
                    vantaggi = sotto_categoria["vantaggi"]
                    svantaggi = sotto_categoria["svantaggi"]

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
    # Dati JSON
    json_data = {
        "tecniche": [
            {
                "nome": "Marinatura",
                "sotto_categorie": [
                    {
                        "nome": "Marinatura a Infusione Gravitazionale",
                        "vantaggi": "Sapore uniforme e intenso",
                        "svantaggi": "Richiede tecnologia avanzata"
                    },
                    {
                        "nome": "Marinatura Temporale Sincronizzata",
                        "vantaggi": "Completamento rapido senza compromessi",
                        "svantaggi": "Rischi temporali"
                    },
                    {
                        "nome": "Marinatura Psionica",
                        "vantaggi": "Sapori personalizzati",
                        "svantaggi": "Richiede competenze psioniche"
                    },
                    {
                        "nome": "Marinatura tramite Reazioni d'Antimateria Diluite",
                        "vantaggi": "Penetrazione rapida e retrogusto cosmico",
                        "svantaggi": "Manipolazione rischiosa"
                    },
                    {
                        "nome": "Marinatura Sotto Zero a Polarità Inversa",
                        "vantaggi": "Massima conservazione dei profumi",
                        "svantaggi": "Necessita di tecnologia avanzata"
                    }
                ]
            },
            {
                "nome": "Affumicatura",
                "sotto_categorie": [
                    {
                        "nome": "Affumicatura a Stratificazione Quantica",
                        "vantaggi": "Penetrazione uniforme",
                        "svantaggi": "Richiede operatori esperti"
                    },
                    {
                        "nome": "Affumicatura Temporale Risonante",
                        "vantaggi": "Sapore profondo e complesso",
                        "svantaggi": "Rischi di disallineamento temporale"
                    },
                    {
                        "nome": "Affumicatura Psionica Sensoriale",
                        "vantaggi": "Sapore adattabile ai gusti individuali",
                        "svantaggi": "Richiede esperti psionici"
                    },
                    {
                        "nome": "Affumicatura tramite Big Bang Microcosmico",
                        "vantaggi": "Intensità unica",
                        "svantaggi": "Operazione rischiosa"
                    },
                    {
                        "nome": "Affumicatura Polarizzata a Freddo Iperbarico",
                        "vantaggi": "Aroma ben conservato",
                        "svantaggi": "Nessuno specifico"
                    }
                ]
            },
            {
                "nome": "Fermentazione",
                "sotto_categorie": [
                    {
                        "nome": "Fermentazione Quantica a Strati Multiversali",
                        "vantaggi": "Sapori unici",
                        "svantaggi": "Rischio di invasioni aliene"
                    },
                    {
                        "nome": "Fermentazione Temporale Sincronizzata",
                        "vantaggi": "Riduzione tempi di fermentazione",
                        "svantaggi": "Possibili instabilità cronologiche"
                    },
                    {
                        "nome": "Fermentazione Psionica Energetica",
                        "vantaggi": "Personalizzazione estrema",
                        "svantaggi": "Richiede esperti psionici"
                    },
                    {
                        "nome": "Fermentazione tramite Singolarità",
                        "vantaggi": "Intensità e complessità uniche",
                        "svantaggi": "Richiede controlli scrupolosi"
                    },
                    {
                        "nome": "Fermentazione Quantico Biometrica",
                        "vantaggi": "Risultati equilibrati e freschi",
                        "svantaggi": "Rischi temporanei per la realtà"
                    }
                ]
            },
            {
                "nome": "Tecniche di Impasto",
                "sotto_categorie": [
                    {
                        "nome": "Impasto Gravitazionale Vorticoso",
                        "vantaggi": "Consistenza perfetta e omogenea",
                        "svantaggi": "Richiede regolazione precisa delle forze gravitazionali"
                    },
                    {
                        "nome": "Amalgamazione Sintetica Molecolare",
                        "vantaggi": "Perfetta fusione di sapori e texture",
                        "svantaggi": "Richiede conoscenza avanzata delle interazioni chimiche"
                    },
                    {
                        "nome": "Impasto a Campi Magnetici Dualistici",
                        "vantaggi": "Ideale per preparazioni a strati complessi",
                        "svantaggi": "Necessita di controllo accurato dei campi magnetici"
                    },
                    {
                        "nome": "Sinergia Elettro-Osmotica Programmabile",
                        "vantaggi": "Controllo totale sull'idratazione",
                        "svantaggi": "Richiede monitoraggio continuo dei parametri"
                    },
                    {
                        "nome": "Modellatura Onirica Tetrazionale",
                        "vantaggi": "Creazioni culinarie uniche ed evocative",
                        "svantaggi": "Richiede manipolatori specializzati dell'onirismo culinario"
                    }
                ]
            }
        ]
    }

    # Inserire i dati nel database
    insert_data(json_data)