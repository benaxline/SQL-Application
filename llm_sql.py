import os
import sqlite3
import traceback
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_db_schema(conn: sqlite3.Connection):
    """
    retrieve the scheme (tables and columns) for the given SQLite connnection
    :param conn: SQLite connection
    :return: a string summarizing the schema for the LLM
    """
    cursor = conn.cursor()

    schema_str = ""

    # get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        schema_str += f'Table: {table_name}\nColumns:\n'

        # get columns
        cursor.execute(f'PRAGMA table_info({table_name});')
        columns = cursor.fetchall()
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            schema_str += f'    - {col_name} ({col_type})\n'
        schema_str += "\n"
    return schema_str


def generate_sql_with_llm(schema_str: str, user_request: str):
    """
    given a schema and a request from the user in plain english, ask LLM to generate SQL

    :param schema_str: SQLite schema
    :param user_request: plain english user request
    :return: SQL query from the LLM as a string
    """
    prompt = f"""
        You are a helpful assistant that can translate natural language into SQL queries for a SQLite database.
        Here is the database schema: 
        {schema_str}
        
        The user wants: {user_request}
        
        Return ONLY the SQL query you think best answers the user's request.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs valid SQL based on the user's request."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.0
        )
        sql_query = response.choices[0]["message"]["content"].strip()
        return sql_query

    except Exception as e:
        with open("error_log.txt", "a") as log_file:
            log_file.write("Error generating SQL with LLM:\n")
            log_file.write(f"{traceback.format_exc()}\n")
        print(f"Error generating SQL with LLM: {e}. See error_log.txt for details.")
        return None


