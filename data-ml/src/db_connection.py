import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="saisanjanas24",
        database=" electronics_manufacturing_db"
    )

    return connection
if __name__ == "__main__":
    connection = get_connection()

    if connection.is_connected():
        print("MYSQL CONNECTION SUCCESSFUL")

    connection.close()