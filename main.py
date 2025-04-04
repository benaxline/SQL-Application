from CLI_assistant import interactive_cli
from csv_to_sql import create_table_from_csv


def main():
    csv_path = 'test.csv'
    table_name = 'test_table'
    db_name = 'testing.db'
    interactive_cli(db_path='testing.db')


main()