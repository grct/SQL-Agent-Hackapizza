import csv
import json
from tqdm import tqdm

with open("../docs/domande.csv", "r") as f:
    # Read the file csv
    csv_reader = csv.reader(f)
    # Read the data
    questions = [row[0] for row in csv_reader][1:]

with open("../docs/dish_mapping.json", "r") as f:
    # Read the file json
    json_data = json.load(f)


results = []
default_value = 50
# Salvare i risultati
for q in tqdm(questions, desc="Processing questions"):
    print("Domanda:", q)
    # RISPOSTA
    result = None
    try:
        pass
    except Exception as e:
        pass

    if result is None:
        result = default_value
    results.append(result)

# Salvare i risultati
with open("risultati.csv", "w") as f:
    # Write the file csv
    csv_writer = csv.writer(f)
    # Write the data
    csv_writer.writerow(["risultato"])
    for r in results:
        csv_writer.writerow([r])