import csv

with open("test.csv", "r") as f:
    data = csv.reader(f)
    results = [row[0] for row in data]

print(len(results))

i=1
with open("result_formatted.csv", "w") as f:
    csv_writer = csv.writer(f)

    csv_writer.writerow(["row_id","result"])

    for r in results:
        r = '"' + r + '"'
        f.write(f"{i},{r}\n")
        i+=1

print("Done")