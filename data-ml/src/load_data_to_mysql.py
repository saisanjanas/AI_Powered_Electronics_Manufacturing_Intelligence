import pandas as pd
from pathlib import Path
from db_connection import get_connection


# Location of generated CSV files
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "generated"


def load_table(connection, csv_name, table_name):
    file_path = DATA_PATH / csv_name

    df = pd.read_csv(file_path)

    columns = list(df.columns)
    column_names = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    query = f"""
        INSERT INTO {table_name} ({column_names})
        VALUES ({placeholders})
    """

    cursor = connection.cursor()

    rows = []

    for row in df.itertuples(index=False, name=None):
        rows.append(
            tuple(None if pd.isna(value) else value for value in row)
        )

    cursor.executemany(query, rows)
    connection.commit()

    cursor.close()

    print(f"{table_name}: {len(df)} rows loaded")


def main():
    connection = get_connection()

    try:
        print("Connected to MySQL")
        print()

        # Load main data tables
        load_table(connection, "production.csv", "production")
        load_table(connection, "production_targets.csv", "production_targets")
        load_table(connection, "quality.csv", "quality")
        load_table(connection, "sensors.csv", "sensors")
        load_table(connection, "downtime.csv", "downtime")
        load_table(connection, "maintenance.csv", "maintenance")
        load_table(connection, "production_logs.csv", "production_logs")

        # Replace old inventory data
        cursor = connection.cursor()
        cursor.execute("DELETE FROM inventory")
        connection.commit()
        cursor.close()

        load_table(connection, "inventory.csv", "inventory")

        print()
        print("ALL DATA LOADED SUCCESSFULLY")

    except Exception as error:
        connection.rollback()
        print("ERROR:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    main()