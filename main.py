from CLI_assistant import interactive_cli, interative_cli_with_llm
from csv_to_sql import create_table_from_csv


def main():
    csv_path = 'test.csv'
    table_name = 'test_table'
    db_name = 'testing.db'
    # interactive_cli(db_path='testing.db')
    interative_cli_with_llm(db_path=db_name)


main()