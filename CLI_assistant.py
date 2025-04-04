import sqlite3
import traceback

from csv_to_sql import create_table_from_csv
from llm_sql import get_db_schema, generate_sql_with_llm


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

def interative_cli_with_llm(db_path='defaultDB.db'):
    """
    A CLI that supports:
      - Loading CSV
      - Listing tables
      - Querying with direct SQL
      - Querying with natural language via an LLM
      - Exiting

    :param db_path: database path
    :return: None
    """
    print('Welcome to the SQLite CLI Assistant!')
    print('Type "help" to see available commands')

    # keep single connection open for the session
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    while True:
        command = input("\nEnter a command (load, list, query, aiquery, help, exit): ").strip().lower()

        if command == 'help':
            print("Available commands:")
            print("  load    - Load a CSV file into a new or existing table.")
            print("  list    - List all tables in the database.")
            print("  query   - Run a SQL query (e.g., SELECT * FROM table).")
            print("  aiquery - Describe your request in plain English; let the LLM generate SQL.")
            print("  exit    - Exit the application.")

        elif command == 'load':
            csv_path = input("Enter the path to the CSV file: ").strip()
            table_name = input("Enter the desired table name: ").strip()
            create_table_from_csv(csv_path, table_name, db_path=db_path)

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

        elif command == 'query':
            sql_query = input("Enter your SQL query: ").strip()
            try:
                cursor.execute(sql_query)
                if sql_query.lower().startswith("select"):
                    rows = cursor.fetchall()
                    for row in rows:
                        print(row)
                else:
                    conn.commit()
                    print("Query executed successfully.")
            except Exception as e:
                with open("error_log.txt", "a") as log_file:
                    log_file.write("An error occurred while executing query:\n")
                    log_file.write(f"{traceback.format_exc()}\n")
                print(f"Error executing query: {e}. See error_log.txt for details.")

        elif command == 'aiquery':
            user_request = input("Describe what you want to do (in plain English): ")
            # 1) Get schema as a string
            schema_str = get_db_schema(conn)
            # 2) Generate SQL from user_request + schema
            sql_query = generate_sql_with_llm(schema_str, user_request)

            if not sql_query:
                print("No SQL query generated.")
                continue

            print(f"\nThe LLM suggests this SQL:\n{sql_query}\n")
            confirm = input("Do you want to run this query? (y/n) ").strip().lower()
            if confirm == 'y':
                try:
                    cursor.execute(sql_query)
                    if sql_query.lower().startswith("select"):
                        rows = cursor.fetchall()
                        for row in rows:
                            print(row)
                    else:
                        conn.commit()
                        print("Query executed successfully.")
                except Exception as e:
                    with open("error_log.txt", "a") as log_file:
                        log_file.write("An error occurred while executing LLM-generated query:\n")
                        log_file.write(f"{traceback.format_exc()}\n")
                    print(f"Error executing query: {e}. See error_log.txt for details.")
            else:
                print("Query canceled.")

        elif command == 'exit':
            print("Exiting the application.")
            break

        else:
            print("Invalid command. Type 'help' for a list of commands.")

    conn.close()
