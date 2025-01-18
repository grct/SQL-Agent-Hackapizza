from src.settings import connect_to_db


def insert_data(json_data):
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            # Query per inserire i dati
            query = """
                INSERT INTO LICENZE (nome, sigla, livello)
                VALUES (%s, %s, %s)
            """

            for licenza in json_data:
                nome = licenza["nome"]
                sigla = licenza["sigla"]
                livello = str(licenza["livello"])

                # Eseguire la query di inserimento
                cursor.execute(query, (nome, sigla, livello))

            # Salvare le modifiche
            connection.commit()

    except Exception as e:
        print(f"Errore durante l'inserimento dei dati: {e}")
        connection.rollback()

    finally:
        connection.close()


if __name__ == "__main__":
    json_data = [
      {
        "nome": "Psionica",
        "sigla": "P",
        "livello": 0,
        "descrizione": "Posseduta da tutti se non diversamente specificato. Tipica degli esseri senzienti."
      },
      {
        "nome": "Psionica",
        "sigla": "P",
        "livello": 1,
        "descrizione": "Lettura pensiero, telecinesi e teletrasporto di oggetti di massa inferiore a 5 kg, precognizione e visione del passato fino a 5 minuti."
      },
      {
        "nome": "Psionica",
        "sigla": "P",
        "livello": 2,
        "descrizione": "Manipolazione della probabilità, telecinesi e teletrasporto di oggetti di massa inferiore a 20 kg, manipolazione delle forze fondamentali dell'universo."
      },
      {
        "nome": "Psionica",
        "sigla": "P",
        "livello": 3,
        "descrizione": "Capacità di donare la coscienza e l'intelletto ad oggetti, manipolazione della realtà circoscritta a stanze, teletrasporto senza errore in qualsiasi dimensione temporale, comunione con entità di altri piani."
      },
      {
        "nome": "Psionica",
        "sigla": "P",
        "livello": 4,
        "descrizione": "Proiezione astrale, riscrittura di realtà circoscritta a piccole nazioni o asteroidi."
      },
      {
        "nome": "Psionica",
        "sigla": "P",
        "livello": 5,
        "descrizione": "Riscrittura di realtà di intere linee temporali o galassie. Questo livello è equivalente al Grado di influenza di livello tecnologico III (LTK III)."
      },
      {
        "nome": "Temporale",
        "sigla": "t",
        "livello": 1,
        "descrizione": "Effetti temporali relativi al presente come dilatazione o accelerazione del tempo."
      },
      {
        "nome": "Temporale",
        "sigla": "t",
        "livello": 2,
        "descrizione": "Livello I + effetti temporali che riguardano linee temporali future."
      },
      {
        "nome": "Temporale",
        "sigla": "t",
        "livello": 3,
        "descrizione": "Livello II + effetti temporali che riguardano linee temporali passate."
      },
      {
        "nome": "Gravitazionale",
        "sigla": "G",
        "livello": 0,
        "descrizione": "5 < G ≤ 10, posseduta da tutti se non diversamente specificato."
      },
      {
        "nome": "Gravitazionale",
        "sigla": "G",
        "livello": 1,
        "descrizione": "0 < G ≤ 100."
      },
      {
        "nome": "Gravitazionale",
        "sigla": "G",
        "livello": 2,
        "descrizione": "0 < G ≤ 10^6."
      },
      {
        "nome": "Gravitazionale",
        "sigla": "G",
        "livello": 3,
        "descrizione": "G > 10^6."
      },
      {
        "nome": "Antimateria",
        "sigla": "e+",
        "livello": 0,
        "descrizione": "Particelle, posseduta da tutti se non diversamente specificato."
      },
      {
        "nome": "Antimateria",
        "sigla": "e+",
        "livello": 1,
        "descrizione": "Antiparticelle."
      },
      {
        "nome": "Magnetica",
        "sigla": "Mx",
        "livello": 0,
        "descrizione": "Polo nord e sud, posseduta da tutti se non diversamente specificato."
      },
      {
        "nome": "Magnetica",
        "sigla": "Mx",
        "livello": 1,
        "descrizione": "Mono-polo."
      },
      {
        "nome": "Quantistica",
        "sigla": "Q",
        "livello": "n",
        "descrizione": "Numero di stati in superposizione dove n è il numero di stati."
      },
      {
        "nome": "Luce",
        "sigla": "c",
        "livello": 1,
        "descrizione": "Solo colori primari (RGB)."
      },
      {
        "nome": "Luce",
        "sigla": "c",
        "livello": 2,
        "descrizione": "Tutto lo spettro visibile umano."
      },
      {
        "nome": "Luce",
        "sigla": "c",
        "livello": 3,
        "descrizione": "Tutte le frequenze."
      },
      {
        "nome": "Livello di Sviluppo Tecnologico",
        "sigla": "LTK",
        "livello": 1,
        "descrizione": "Planetario."
      },
      {
        "nome": "Livello di Sviluppo Tecnologico",
        "sigla": "LTK",
        "livello": 2,
        "descrizione": "Sistema Stellare."
      },
      {
        "nome": "Livello di Sviluppo Tecnologico",
        "sigla": "LTK",
        "livello": 3,
        "descrizione": "Galassia."
      },
      {
        "nome": "Livello di Sviluppo Tecnologico",
        "sigla": "LTK",
        "livello": 4,
        "descrizione": "Superamasso di Galassie."
      },
      {
        "nome": "Livello di Sviluppo Tecnologico",
        "sigla": "LTK",
        "livello": 5,
        "descrizione": "Intero Universo."
      },
      {
        "nome": "Livello di Sviluppo Tecnologico",
        "sigla": "LTK",
        "livello": 6,
        "descrizione": "Universi multipli."
      },
      {
        "nome": "Livello di Sviluppo Tecnologico",
        "sigla": "LTK",
        "livello": "6+",
        "descrizione": "Tutte le fonti energia."
      }
    ]

    insert_data(json_data)