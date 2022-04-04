import sqlite3

from sqlite3 import Error
conn = None

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Hi " +sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    
#if __name__ == '__main__':
    #create_connection(r"C:\sqlite\db\pythonsqlite.db")
    #create_connection(r"db_test.db") # Creates connection to database. Creates a new database file if file does not exist.
    #create table

conn = sqlite3.connect(r"db_test.db")
#with conn:
#    conn.execute("""
#        CREATE TABLE USER (
#                hour INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#                name TEXT,
#                measurement_urine FLOAT
#            );
#        """)

sql = 'INSERT INTO USER (hour, name, measurement_ml) values(?, ?, ?)'
data = [
    (1, 'Bob', 20.5),
    (2, 'Jesse', 25.0),
    (3, 'Jorn', 22.2),
]
#conn.executemany(sql, data)

with conn:
    data = conn.execute("SELECT * FROM USER WHERE measurement_ml <= 23")
    for row in data:
        print(row)


