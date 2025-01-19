from src.settings import connect_to_db
import csv

def populate_distance_matrix():
    connection = connect_to_db()
    with connection.cursor() as cursor:

        # Create the table (if it doesn't exist)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS DISTANZE (
            name1 VARCHAR(255),
            name2 VARCHAR(255),
            distance INT,
            PRIMARY KEY (name1, name2)
        );
        """)

        # Open the CSV file
        with open('Distanze.csv', mode='r') as file:
            reader = csv.reader(file)
            names = next(reader)  # First row is the header (the names)

            # Iterate through each row in the CSV
            for i, row in enumerate(reader):
                for j, distance in enumerate(row[1:], start=1):  # Skip the first column (name)
                    name1 = names[i + 1]  # Get the name from the first column
                    name2 = names[j]  # Get the name from the first row
                    distance_value = int(distance)

                    # Insert the distance data into the table
                    cursor.execute("""
                        INSERT INTO DISTANZE (name1, name2, distance)
                        VALUES (%s, %s, %s)
                        ON DUPLICATE KEY UPDATE distance = VALUES(distance);
                    """, (name1, name2, distance_value))

        # Commit the transaction
        connection.commit()

        # Close the cursor and the connection
        cursor.close()
        connection.close()


if __name__ == "__main__":
    populate_distance_matrix()