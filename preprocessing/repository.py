import json
import pymysql
import os
def connect_to_db():
    return pymysql.connect(
        host="77.37.121.60",
        user="root",
        password="momentumdigital00",
        database="HackaPizza",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def popolate_dishses(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            for k,v in data.items():
                query = """
                        INSERT INTO PIATTI (id, nome)
                        VALUES (%s, %s)
                        ON DUPLICATE KEY UPDATE nome = VALUES(nome)
                        """
                cursor.execute(query, (v, k))
            
            connection.commit()

    except Exception as e:
        print(f"Errore durante l'inserimento dei dati: {e}")
        connection.rollback()

    finally:
        connection.close()
    

def map_dishes(filename):
    # Carica il file JSON
    with open(filename, 'r') as file:
        data = json.load(file)

    connection = connect_to_db()

    try:
        with connection.cursor() as cursor:
            for dish in data['piatti']:
                # Controlla se il piatto esiste nella tabella PIATTI
                check_dish_query = "SELECT id FROM PIATTI WHERE nome like %s"
                cursor.execute(check_dish_query, (f"%{dish['name']}%"))
                dish_result = cursor.fetchone()

                if dish_result:
                    dish_id = dish_result['id']
                else:
                    # Se il piatto non esiste, lo ignora
                    continue

                # Processa gli ingredienti del piatto
                for ingredient in dish['ingredients']:
                    # Controlla se l'ingrediente esiste nella tabella INGREDIENTI
                    check_ingredient_query = "SELECT id FROM INGREDIENTI WHERE nome like %s"
                    cursor.execute(check_ingredient_query, (f"%{ingredient}%"))
                    ingredient_result = cursor.fetchone()

                    if ingredient_result:
                        ingredient_id = ingredient_result['id']
                    else:
                        insert_ingredient_query = """
                            INSERT INTO INGREDIENTI (nome)
                            VALUES (%s)
                        """
                        cursor.execute(insert_ingredient_query, (ingredient))
                        ingredient_id=cursor.lastrowid
                    
                    # Inserisce il mapping tra piatto e ingrediente
                    insert_dish_ingredient_query = """
                            INSERT INTO PIATTI_INGREDIENTI (id_piatto, id_ingrediente)
                            VALUES (%s, %s)
                        """
                    cursor.execute(insert_dish_ingredient_query, (dish_id, ingredient_id))

                # Processa le tecniche del piatto
                for technique in dish['techniques']:
                    # Controlla se la tecnica esiste nella tabella TECNICHE
                    check_technique_query = "SELECT id FROM TECNICHE WHERE descrizione like  %s"
                    cursor.execute(check_technique_query, (f"%{technique}%"))
                    technique_result = cursor.fetchone()

                    if technique_result:
                        technique_id = technique_result['id']
                        # Inserisce il mapping tra piatto e tecnica
                        insert_dish_technique_query = """
                            INSERT INTO PIATTI_TECNICHE (id_piatto, id_tecnica)
                            VALUES (%s, %s)
                        """
                        cursor.execute(insert_dish_technique_query, (dish_id, technique_id))
                    else:
                        # Se la tecnica non esiste, la ignora
                        print(f"Tecnica non trovata: {technique}, ignorata.")

            # Salva le modifiche nel database
            connection.commit()

    except Exception as e:
        print(f"Errore durante il mapping dei piatti: {e}")
        connection.rollback()

    finally:
        connection.close()



def map_restaurant(filename):
    """
    Legge i dati del ristorante dal JSON e:
      1) Inserisce (pianeta, chef) in RISTORANTE
      2) Recupera l'id appena inserito
      3) Per ogni skill del JSON, verifica se esiste una licenza in base a nome o sigla.
         - Se trova la licenza e il livello corrisponde, la mappa in RISTORANTE_LICENZE
      4) Per ogni piatto nel JSON, se esiste in PIATTI, lo mappa nella tabella RISTORANTE_PIATTI
    """
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    connection = connect_to_db()
    try:
        with connection.cursor() as cursor:
            # Estraggo i campi principali del ristorante dal JSON
            chef = data['ristorante'].get('chef', '')
            pianeta = data['ristorante'].get('pianeta', '')

            # Inserisce i dati in RISTORANTE
            insert_query = """
                INSERT INTO RISTORANTE (pianeta, chef)
                VALUES (%s, %s)
            """
            cursor.execute(insert_query, (pianeta, chef))
            connection.commit()
            
            # Recupero l'id del ristorante appena inserito
            ristorante_id = cursor.lastrowid

            # Ora gestiamo le skill => licenze
            if 'skill' in data['ristorante']:
                for skill_item in data['ristorante']['skill']:
                    # Estrai il nome della skill e il livello
                    if 'name' in skill_item:
                        skill_name = skill_item['name']
                        skill_level = skill_item['level']
                    else:
                        skill_name, skill_level = list(skill_item.items())[0]
                    
                    # Cerca prima licenze per nome (LIKE)
                    select_by_nome = """
                        SELECT id, livello 
                        FROM LICENZE
                        WHERE nome LIKE %s
                        AND (livello = %s OR livello = "n")
                    """
                    cursor.execute(select_by_nome, (f"%{skill_name}%",skill_level))
                    found_licenza = cursor.fetchone()
                    
                    if not found_licenza:
                        # Cerca per sigla (LIKE)
                        select_by_sigla = """
                            SELECT id, livello 
                            FROM LICENZE
                            WHERE sigla LIKE %s
                            AND (livello = %s OR livello = "n")
                        """
                        cursor.execute(select_by_sigla, (f"%{skill_name}%",skill_level))
                        found_licenza = cursor.fetchone()
                    
                    # Gestione del risultato della licenza
                    if found_licenza:
                        licenza_id = found_licenza['id']
                        licenza_level = found_licenza['livello']
                        
                        if licenza_level == skill_level or licenza_level == "n":
                            insert_map = """
                                INSERT INTO RISTORANTE_LICENZE (id_ristorante, id_licenza)
                                VALUES (%s, %s)
                            """
                            cursor.execute(insert_map, (ristorante_id, licenza_id))
                            print(f"Licenza '{skill_name}' (livello={skill_level}) associata al ristorante.")
                        else:
                            print(f"Livello non corrispondente per licenza '{skill_name}': "
                                  f"{licenza_level} != {skill_level}. Ignorata.")
                    else:

                        print(f"Skill '{skill_name}' non trovata (né come nome né come sigla). Ignorata.")

            # Ora mappiamo i piatti del ristorante
            if 'piatti' in data:
                for dish in data['piatti']:
                    dish_name = dish.get('name', '')
                    if not dish_name:
                        continue
                    
                    # Controlla se il piatto esiste nella tabella PIATTI (LIKE)
                    check_dish_query = """
                        SELECT id FROM PIATTI 
                        WHERE nome LIKE %s
                    """
                    cursor.execute(check_dish_query, (f"%{dish_name}%",))
                    dish_result = cursor.fetchone()

                    if dish_result:
                        dish_id = dish_result['id']
                        # Inserisce il mapping tra ristorante e piatto
                        insert_ristorante_piatto_query = """
                            INSERT INTO RISTORANTE_PIATTI (id_ristorante, id_piatto)
                            VALUES (%s, %s)
                        """
                        cursor.execute(insert_ristorante_piatto_query, (ristorante_id, dish_id))
                    else:
                        print(f"Piatto '{dish_name}' non trovato in PIATTI. Ignorato.")

            # Conferma tutte le operazioni
            connection.commit()
    
    except Exception as e:
        print(f"Errore durante l'inserimento del ristorante o il mapping di licenze/piatti: {e}")
        connection.rollback()
    finally:
        connection.close()


if __name__ == "__main__":
    # Esegui la funzione con il file JSON fornito
    path= "../docs/json"
    # Itera su tutti i file JSON nella directory
    i=0
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)

        if filename.endswith(".json"):
            print(f"Processing file: {filename} {i}/30")

            try:
                # Lancia le funzioni per ciascun file
                #popolate_dishses(full_path)
                map_dishes(full_path)
                map_restaurant(full_path)
            except Exception as e:
                print(f"Errore nel file {filename}: {e}")
            finally:
                i+=1
            
