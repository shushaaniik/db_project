import psycopg2
from psycopg2 import sql


def initialize_db(db_name, owner_username, owner_password="secret"):
    # Connect to the default database to create a new DB
    connection = psycopg2.connect(
        dbname="postgres_db",
        user="admin",
        password="secret",
        host="localhost",
        port="5432"
    )

    connection.autocommit = True
    cursor = connection.cursor()

    try:
        # Create a new DB
        cursor.execute(sql.SQL(f"CREATE DATABASE {db_name}"))

        connection.close()
        connection = psycopg2.connect(
            dbname="postgres_db",
            user=owner_username,
            password=owner_password,
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()

        print(f"Database '{db_name}' created and owned by '{owner_username}'.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()


if __name__ == "__main__":
    initialize_db(db_name="ConnectionOperators",
                  owner_username="admin",
                  owner_password="secret")
