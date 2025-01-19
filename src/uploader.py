import csv

with open("test.csv", "r") as f:
    data = csv.reader(f)
    results = [row for row in data]

print(len(results))

i=1
with open("risultati_f.csv", "w") as f:
    csv_writer = csv.writer(f)

    csv_writer.writerow(["row_id","result"])

    for r in results:
        r = ",".join(r)
        r = '"' + r + '"'
        f.write(f"{i},{r}\n")
        i+=1

print("Done")