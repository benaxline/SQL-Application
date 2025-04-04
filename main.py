from csv_to_sql import create_table_from_csv


def main():
    csv_path = 'test.csv'
    table_name = 'test_table'
    db_name = 'testing.db'
    create_table_from_csv(csv_path=csv_path, table_name=table_name, db_path=db_name)

main()