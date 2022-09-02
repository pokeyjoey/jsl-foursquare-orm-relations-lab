import psycopg2

test_conn = psycopg2.connect(dbname = 'foursquare_test', user = 'postgres', password = 'postgres')
test_cursor = test_conn.cursor()

def drop_records(cursor, conn, table_name):
    cursor.execute(f"DELETE FROM {table_name};")
    conn.commit()

def drop_tables(table_names, cursor, conn):
    for table_name in table_names:
        drop_records(cursor, conn, table_name)

def drop_all_tables(conn, cursor):
    table_names = ['venue_categories', 'locations', 'zipcodes', 'cities', 'states', 'categories', 'venues']
    drop_tables(table_names, cursor, conn)

