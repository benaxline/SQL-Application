import sqlite3
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
    creates a SQLite from a CSV file

    :param csv_path: path to CSV file
    :param table_name: name of the SQLite table
    :param db_path: path to database file
    :return:
    """
    df = pd.read_csv(csv_path)

    column_types = {}
    for col in df.columns:
        inferred_type = df[col].dtype
        column_types[col] = map_dtype_to_sql(inferred_type)

    columns_def = []
    for col, sql_type in column_types.items():
        columns_def.append(f'"{col}" {sql_type}')  # Quote col name for safety

    columns_str = ",\n  ".join(columns_def)
    create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
          {columns_str}
        )
        """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()

    df.to_sql(table_name, conn, if_exists='append', index=False)

    conn.close()

