import csv
import json

with open("../docs/domande.csv", "r") as f:
    # Read the file csv
    csv_reader = csv.reader(f)
    # Read the data
    questions = [row[0] for row in csv_reader][1:]

with open("../docs/dish_mapping.json", "r") as f:
    # Read the file json
    json_data = json.load(f)

for q in questions:
    print("Domanda:", q)