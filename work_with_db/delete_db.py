import psycopg2
from psycopg2 import sql


def delete_db(db_name):
    try:
        # Connect to the default database to delete the specified DB
        connection = psycopg2.connect(
            dbname="postgres",
            user="admin",
            password="secret",
            host="localhost",
            port="5432"
        )

        connection.autocommit = True
        cursor = connection.cursor()

        cursor.execute(sql.SQL(f"DROP DATABASE IF EXISTS {db_name}"))

        print(f"Database '{db_name}' deleted.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


if __name__ == "__main__":
    delete_db(db_name="ConnectionOperators")
