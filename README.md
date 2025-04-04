# SQL-Application

Using OpenAI as the chat interface. 

Upload CSV file which will be translated into SQL tables.

Through the chat, we can query the database.

### Function Explainations

- `map_dtype_to_sql`: This function maps the inferred datatype found in the CSV column to the SQLite data type (Integer, Real, or text).
- `create_table_from_csv`: This function creates a SQLite table from a CSV file.