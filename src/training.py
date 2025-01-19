import os

folder_path = r'../docs/vanna'

def training(vn):
    vn.connect_to_mysql(host=os.getenv('DB_HOST'), dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'), port=3306)
    vn.train(
        documentation="Il database che stai visualizzando contiene tutti i ristoranti, piatti e tecniche utilizzati nei diversi pianeti del Ciclo Cosmico. ")

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            full_path = os.path.join(folder_path, file_name)
            with open(full_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    vn.train(documentation=line.strip())

    vn.train(question="Quali sono i piatti che includono le Chocobo Wings come ingrediente?",
             sql="""
                        SELECT id_piatto FROM PIATTI_INGREDIENTI PI
                        INNER JOIN INGREDIENTI I ON PI.id_ingrediente = I.id
                        WHERE I.nome LIKE '%Chocobo%' 
                    """)
    vn.train(question="Trova i piatti che utilizzano la tecnica Marinatura a Infusione",
             sql="""
                        select PT.id_piatto from PIATTI_TECNICHE PT
                        INNER JOIN TECNICHE T ON PT.id_tecnica = T.id
                         where T.descrizione LIKE '%Marinatura a infusione%'
                    """)
    vn.train(question="Quali sono i piatti disponibili nei ristoranti entro 126 anni luce da Cybertron, quest ultimo incluso, che non includono Funghi dell Etere?",
             sql="""
                            SELECT DISTINCT 
                                p.id
                            FROM RISTORANTE r
                            JOIN (
                                SELECT 
                                    CASE 
                                        WHEN name1 = 'Cybertron' THEN name2
                                        WHEN name2 = 'Cybertron' THEN name1
                                    END AS pianeta,
                                    distance
                                FROM DISTANZE
                                WHERE 'Cybertron' IN (name1, name2)
                            ) d ON r.pianeta = d.pianeta
                            JOIN RISTORANTE_PIATTI rp ON r.id = rp.id_ristorante
                            JOIN PIATTI p ON p.id = rp.id_piatto
                            WHERE d.distance <= 126
                            AND NOT EXISTS (
                                SELECT 1 
                                FROM PIATTI_INGREDIENTI pi
                                JOIN INGREDIENTI i ON i.id = pi.id_ingrediente
                                WHERE pi.id_piatto = p.id 
                                AND i.nome = 'Funghi dell''Etere'
                            )
                        """)




