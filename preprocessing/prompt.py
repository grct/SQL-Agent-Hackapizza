restaurant_prompt = '''
                Analizza il menu fornito e recupera solo queste due informazioni:
                - Nome del ristorante
                - Nome dello Chef

                {format_instructions}

                Menu:
                {text}
'''

skill_prompt = '''
                Partendo da questo documento rappresentante il menù di un ristorante appartenente ad una galassia inventata, estrai il livello (o grado) per ogni Abilità(skill) o Licenze, selezionando tra le seguenti:

                Abilità e Licenze Richieste
                Prima di iniziare a cucinare nello spazio, è fondamentale ottenere le giuste autorizzazioni e raggiungere legiuste abilità. Non ci si può semplicemente mettere ai fornelli gravitazionali senza essere certificati: ci
                sono normative severe che regolano ogni fase della preparazione e gestione del cibo a bordo di una nave
                spaziale. Ovviamente, non ho mai cucinato senza la giusta licenza (non lo farei mai per nessun motivo).
                Vediamo insieme le principali licenze richieste nel formato nome, sigla, livello: 
                    "Psionica";"P";"0"
                    "Psionica";"P";"1"
                    "Psionica";"P";"2"
                    "Psionica";"P";"3"
                    "Psionica";"P";"4"
                    "Psionica";"P";"5"
                    "Temporale";"t";"1"
                    "Temporale";"t";"2"
                    "Temporale";"t";"3"
                    "Gravitazionale";"G";"0"
                    "Gravitazionale";"G";"1"
                    "Gravitazionale";"G";"2"
                    "Gravitazionale";"G";"3"
                    "Antimateria";"e+";"0"
                    "Antimateria";"e+";"1"
                    "Magnetica";"Mx";"0"
                    "Magnetica";"Mx";"1"
                    "Quantistica";"Q";"n"
                    "Luce";"c";"1"
                    "Luce";"c";"2"
                    "Luce";"c";"3"
                    "Livello di Sviluppo Tecnologico";"LTK";"1"
                    "Livello di Sviluppo Tecnologico";"LTK";"2"
                    "Livello di Sviluppo Tecnologico";"LTK";"3"
                    "Livello di Sviluppo Tecnologico";"LTK";"4"
                    "Livello di Sviluppo Tecnologico";"LTK";"5"
                    "Livello di Sviluppo Tecnologico";"LTK";"6"
                    "Livello di Sviluppo Tecnologico";"LTK";"6+"

                Recupera queste informazioni:
                - skillName : nome corretto della skill
                - level: livello della skill scritto in numeri ordinari, NON ROMANI
                queste informazioni possono essere contenute dentro al testo o in apposite list a bullet point.
                
                
                {format_instructions}

                Menu:
                {text}
'''

dish_prompt = '''
                Analizza il menu e recupera queste informazioni per ogni piatto presente:
                - Il nome del piatto
                - La lista degli ingredienti sotto la sezione "Ingredienti" o all'interno della descrizione
                - La lista delle tecniche sotto la sezione "Tecniche" o all'interno della descrizione
                
                Le tecniche possono essere SOLO tra queste:
                    Marinatura a Infusione Gravitazionale
                    Marinatura Temporale Sincronizzata
                    Marinatura Psionica
                    Marinatura tramite Reazioni d'Antimateria Diluite
                    Marinatura Sotto Zero a Polarita Inversa
                    Affumicatura a Stratificazione Quantica
                    Affumicatura Temporale Risonante
                    Affumicatura Psionica Sensoriale
                    Affumicatura tramite Big Bang Microcosmico
                    Affumicatura Polarizzata a Freddo Iperbarico
                    Fermentazione Quantica a Strati Multiversali
                    Fermentazione Temporale Sincronizzata
                    Fermentazione Psionica Energetica
                    Fermentazione tramite Singolarita
                    Fermentazione Quantico Biometrica
                    Impasto Gravitazionale Vorticoso
                    Amalgamazione Sintetica Molecolare
                    Impasto a Campi Magnetici Dualistici
                    Sinergia Elettro-Osmotica Programmabile
                    Modellatura Onirica Tetrazionale


                {format_instructions}

                Menu:
                {text}


'''