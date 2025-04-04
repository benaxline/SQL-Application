import sqlite3
import traceback

from csv_to_sql import create_table_from_csv


def interactive_cli(db_path=f'defaultDB.db'):
    """
    simple SLI assistant that lets the user
        - Load a CSV file into the DB
        - Run SQL queries
        - List tables
        - exit

    :param db_path: SQLite path
    :return: None
    """
    print('Welcome to the SQLite CLI Assistant!')
    print('Type "help" to see available commands')

    # keep single connection open for the session
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    while True:
        command = input('\nEnter a command (load, query, list, help, exit): ').strip().lower()

        if command == 'help':
            print("Available commands:")
            print("  load  - Load a CSV file into a new or existing table.")
            print("  query - Run a SQL query (e.g., SELECT * FROM table).")
            print("  list  - List all tables in the database.")
            print("  exit  - Exit the application.")

        elif command == 'load':
            csv_path = input("Enter the path to the CSV file: ").strip()
            table_name = input("Enter the desired table name: ").strip()
            create_table_from_csv(csv_path, table_name, db_path=db_path)

        elif command == 'query':
            sql_query = input("Enter your SQL query: ").strip()
            try:
                cursor.execute(sql_query)

                # If it's a SELECT query, fetch results
                if sql_query.lower().startswith("select"):
                    rows = cursor.fetchall()
                    # Print rows in a basic table format
                    for row in rows:
                        print(row)
                else:
                    # For UPDATE/DELETE/INSERT statements
                    conn.commit()
                    print("Query executed successfully.")
            except Exception as e:
                # Log to file and display error
                with open("error_log.txt", "a") as log_file:
                    log_file.write("An error occurred while executing query:\n")
                    log_file.write(f"{traceback.format_exc()}\n")
                print(f"Error executing query: {e}. See error_log.txt for details.")

        elif command == 'list':
            try:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                if tables:
                    print("Tables in the database:")
                    for t in tables:
                        print(f"  {t[0]}")
                else:
                    print("No tables found in the database.")
            except Exception as e:
                with open("error_log.txt", "a") as log_file:
                    log_file.write("An error occurred while listing tables:\n")
                    log_file.write(f"{traceback.format_exc()}\n")
                print(f"Error listing tables: {e}. See error_log.txt for details.")

        elif command == 'exit':
            print("Exiting the application.")
            break

        else:
            print("Invalid command. Type 'help' for a list of commands.")

    conn.close()

