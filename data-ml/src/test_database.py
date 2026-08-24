from db_connection import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("SHOW TABLES")

print("TABLES IN DATABASE:")

for table in cursor:
    print(table[0])

cursor.close()
connection.close()