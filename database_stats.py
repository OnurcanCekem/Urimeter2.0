# Program for database
# v1.1 2022-04-11: Changed table, added function to add data or delete data by id and name.
# v1.2 2022-04-11: added function to delete most recent insert and data by measurement.


import sqlite3

from sqlite3 import Error
from time import gmtime, strftime
conn = None

# Function to check the db connection.
# Kinda not needed if you ask me.
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

# Add data to database
# Parameter Patient_ID: The ID of a patient
# Parameter name: The name of a patient
# Parameter Measurement_ML: The current measured urine
def add_data(Patient_ID, name, Measurement_ML):
    data_add = (Patient_ID, name, strftime("%Y-%m-%d %H:%M:%S", gmtime()), Measurement_ML) # create case to store data
    conn.execute('INSERT OR IGNORE INTO PATIENT_STATS (Patient_ID, Patient_Name, Timestamp, Measurement_ML) values(?, ?, ?, ?)', data_add) # add data in database
    
    #Test variable
    #data_add = ( 1, 'Bob', strftime("%Y-%m-%d %H:%M:%S", gmtime()), 31.2) # create case to store data


# Delete a patient by ID
# Parameter Patient_ID: The ID of a patient
def delete_ID(Patient_ID):
    condition = 'DELETE FROM PATIENT_STATS WHERE Patient_ID=?' # select the condition for patient_id
    conn.execute(condition, (Patient_ID,)) # execute the condition

# Delete a patient by name
# Parameter name: The name of a patient
def delete_Name(Name):
    condition = 'DELETE FROM PATIENT_STATS WHERE Patient_Name=?' # select the name
    conn.execute(condition, (Name,)) # execute the condition

# Delete a patient by name
# Parameter name: The name of a patient
def delete_Measurement(Measurement):
    condition = 'DELETE FROM PATIENT_STATS WHERE Measurement_ML=?' # select the name
    conn.execute(condition, (Measurement,)) # execute the condition

# Delete the most recent insert from the database.
def delete_Latest():
    condition = 'DELETE FROM PATIENT_STATS WHERE ID=(SELECT MAX(ID) FROM PATIENT_STATS)' # select the highest ID which is the latest insert
    conn.execute(condition,) # execute the condition


# IDK what to do with this one
#if __name__ == '__main__':
    #create_connection(r"C:\sqlite\db\pythonsqlite.db")
    #create_connection(r"db_test.db") # Creates connection to database. Creates a new database file if file does not exist.
    #create table

conn = sqlite3.connect(r"db_test.db") # Connect to the database

# Create database table
#with conn:
#    conn.execute("""
#        CREATE TABLE PATIENT_STATS (
#                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#                Patient_ID INTEGER, 
#                Patient_Name VARCHAR(255),
#                Timestamp datetime,
#                Measurement_ML FLOAT
#             );
#            """)


# Insert multiple data to database
#sql = 'INSERT INTO USER (hour, name, measurement_ml) values(?, ?, ?)'
#data = [
#    (1, 1, 'Bob', 1, 20.5),
#    (2, 1, 'Bob', 2, 25.0),
#    (3, 1, 'Bob', 3, 22.2),
#    (4, 2, 'Jesse', 1, 21.2),
#    (5, 2, 'Jesse', 2, 25.2),
#    (6, 3, 'Jeroen', 2, 20.2),
#    (7, 2, 'Jesse', 3, 18.5),
#]
#conn.executemany(sql, data)


# Print out current time and date
#print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

# Add single data
#data_add = (1, 1, 'Bob', strftime("%Y-%m-%d %H:%M:%S", gmtime()), 32.2) # create case to store data
#conn.execute('INSERT INTO PATIENT_STATS (ID, Patient_ID, Patient_Name, Timestamp, Measurement_ML) values(?, ?, ?, ?, ?)', data_add) # add data in database
add_data(2, 'Jesse', 29.7)
#==================================================
#Print before something
with conn:
    data = conn.execute("SELECT * FROM PATIENT_STATS")
    print("before:")
    for row in data:
        print(row)
#==================================================
#Do something
#add_data(2, 'Jesse', 28.1)
#delete_Name('Onurcan')
delete_Measurement(29.7)
#==================================================
#Print after something
with conn:
    data = conn.execute("SELECT * FROM PATIENT_STATS")
    #data = conn.execute("SELECT * FROM PATIENT_STATS WHERE measurement_ml >= 23")
    print("\n\nafter:")
    for row in data:
        print(row)
#==================================================


conn.close() # close connection with database