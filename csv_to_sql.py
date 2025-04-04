import sqlite3
import traceback

import pandas as pd

def map_dtype_to_sql(dtype):
    """
    maps a dtype to sql data type

    :param dtype: the datatype
    :return: sql data type as a string
    """
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    else:
        return "TEXT"


def create_table_from_csv(csv_path: str, table_name: str, db_path: str=f'defaultDB.db'):
    """
    creates or updates a SQLite table from a CSV file.
    - checks existing table schema via PRAGMA table_info()
    - prompting user for overwrite/rename/skip if conflict
    - Logging errors to error_log.txt

    :param csv_path: path to CSV file
    :param table_name: name of the SQLite table
    :param db_path: path to database file
    :return: None
    """
    try:
        # read dataframe
        df = pd.read_csv(csv_path)

        # infer column type
        column_types = {}
        for col in df.columns:
            inferred_type = df[col].dtype
            column_types[col] = map_dtype_to_sql(inferred_type)

        # connect to SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # check if table already exists
        cursor.execute(f"PRAGMA table_info({table_name});")
        existing_schema = cursor.fetchall()

        if existing_schema:
            # table exists
            print(f"Table '{table_name}' already exists in {db_path}.")
            action = ""
            valid_actions = {"o": "overwrite",
                             "r": "rename",
                             "s": "skip"}
            while action not in valid_actions:
                action = input("Choose action: [O]verwrite, [R]ename, or [S]kip? ").lower()

            if action == "o":
                # overwrite
                print(f'Overwriting table "{table_name}"...')
                cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
            elif action == "r":
                # rename
                new_name = input('Enter new table name: ').strip()
                print(f'WIll create a new table "{new_name}" instead of "{table_name}".')
                table_name = new_name
            else:
                # Skip
                print('Skipping table creation. Exiting function.')
                conn.close()
                return

        # create table statement
        columns_def = []
        for col, sql_type in column_types.items():
            columns_def.append(f'"{col}" {sql_type}')  # Quote col name for safety

        columns_str = ",\n  ".join(columns_def)
        create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
              {columns_str}
            )
            """

        # create new table
        cursor.execute(create_table_sql)
        conn.commit()

        # insert data from DF
        df.to_sql(table_name, conn, if_exists='append', index=False)

        conn.close()
        print(f'Table "{table_name}" successfully created/updated in {db_path}.')

    except Exception as e:
        with open("error_log.txt", 'a') as log_file:
            log_file.write("An error occurred:\n")
            log_file.write(f'{traceback.format_exc()}\n')
        print(f'AN error occurred: {e}. Details logged to error_log.txt.')


