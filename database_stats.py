"""
 * database_stats.py
 *
 *  Created on: April 4, 2022
 *  Last update: June 30, 2022
 *      Author: onurc
 *  Description: Program with database functionality. Can uncomment for creating database and outputting debug values. 
                 Mainly used for understanding the existing database.
                To get started look at the following: create database and create table.
 """
# v1.1 2022-04-11: Changed table, added function to add data or delete data by id and name.
# v1.2 2022-04-11: added function to delete most recent insert and data by measurement.


import sqlite3
import random # for RNGesus

from sqlite3 import Error
from time import gmtime, strftime
import datetime
conn = None # Variable to use as connection with the database

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
    data_add = (Patient_ID, name, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), Measurement_ML) # create case to store data
    conn.execute('INSERT OR IGNORE INTO PATIENT_STATS (Patient_ID, Patient_Name, Timestamp, Measurement_ML) values(?, ?, ?, ?)', data_add) # add data in database
    
    # Test variables create case to store data
    #data_add = ( 1, 'Bob', strftime("%Y-%m-%d %H:%M:%S", gmtime()), 31.2) # without parameters
    #data_add = (Patient_ID, name, strftime("%Y-%m-%d %H:%M:%S", gmtime()), Measurement_ML) # with parameters


# Delete a patient by ID
# Parameter Patient_ID: The ID of a patient
def delete_Patient_ID(Patient_ID):
    condition = 'DELETE FROM PATIENT_STATS WHERE Patient_ID=?' # select the condition for patient_id
    conn.execute(condition, (Patient_ID,)) # execute the condition

# Delete a patient by name
# Parameter name: The name of a patient
def delete_Name(Name):
    condition = 'DELETE FROM PATIENT_STATS WHERE Patient_Name=?' # select the name
    conn.execute(condition, (Name,)) # execute the condition

# Delete a patient by Measurement
# Parameter Measurement: The measured amount of urine in ml
def delete_Measurement(Measurement):
    condition = 'DELETE FROM PATIENT_STATS WHERE Measurement_ML=?' # select the name
    conn.execute(condition, (Measurement,)) # execute the condition

# Delete the most recent insert from the database.
def delete_Latest():
    condition = 'DELETE FROM PATIENT_STATS WHERE ID=(SELECT MAX(ID) FROM PATIENT_STATS)' # select the highest ID which is the latest insert
    conn.execute(condition,) # execute the condition

# Untested function
def delete_All():
    condition = 'DELETE FROM PATIENT_STATS)' # select the highest ID which is the latest insert
    conn.execute(condition,) # execute the condition

# Get all rows with Patient_ID
# Parameter Patient_ID: The ID of a patient
def get_Patient_ID(Patient_ID):
    data = conn.execute("SELECT * FROM PATIENT_STATS WHERE Patient_ID=?", (Patient_ID,)) # retrieve all rows with Patient_ID
    return data

# Get all rows with Patient_Name
# Parameter Patient_Name: The name of a patient
def get_Patient_Name(Patient_Name):
    data = conn.execute("SELECT * FROM PATIENT_STATS WHERE Patient_Name=?", (Patient_Name,)) # retrieve all rows with Patient_ID
    return data

# Get all rows with Measurement
# Parameter Measurement: The measured amount of urine in ml
def get_Measurement(Measurement):
    data = conn.execute("SELECT * FROM PATIENT_STATS WHERE Measurement_ML=?", (Measurement,)) # retrieve all rows with Patient_ID
    return data

# Get the most recent insert from the database.
def get_Latest():
    data = conn.execute("SELECT * FROM PATIENT_STATS WHERE ID=(SELECT MAX(ID) FROM PATIENT_STATS)") # retrieve all rows with Patient_ID
    return data

# Get all measurements in the past 24 hours from given Patient ID.
# Parameter Patient_ID: The ID of a patient
def get_24hours(Patient_ID):
    data = conn.execute("SELECT * FROM PATIENT_STATS WHERE Timestamp > datetime('now', '-1 day') AND Patient_ID=?", (Patient_ID,)) # retrieve all rows in the past 24hrs with Patient_ID
    return data

# ==============================================================
# Create database file
# ==============================================================
# Create database file if it doesn't exist. Uncomment to create this file if you don't have one.
#if __name__ == '__main__':
    #create_connection(r"C:\sqlite\db\pythonsqlite.db")
    #create_connection(r"db_test.db") # Creates connection to database. Creates a new database file if file does not exist.
    #create table

conn = sqlite3.connect(r"db_test.db") # Connect to the database

# ==============================================================
# Create table
# ==============================================================
# Uncomment to create table. Run it once, or it generates errors as it tries to make another table when it already exists.
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

# Print out current time and date
#print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

# Add single data example
#data_add = (1, 1, 'Bob', strftime("%Y-%m-%d %H:%M:%S", gmtime()), 32.2) # create case to store data
#conn.execute('INSERT INTO PATIENT_STATS (ID, Patient_ID, Patient_Name, Timestamp, Measurement_ML) values(?, ?, ?, ?, ?)', data_add) # add data in database

#==================================================
#Print before something
if __debug__:
    with conn:
        data = conn.execute("SELECT * FROM PATIENT_STATS")
        print("before:")
        for row in data:
            print(row)
        print("\n")
#==================================================
# Do something
#add_data(2, 'Jesse', 28.1)
#delete_Name('Onurcan')
#delete_Measurement(29.7)
#get_Patient_ID(1)
#add_data(2, 'Jesse', 29.5)
add_data(2, 'Jesse', round(random.uniform(15,50),1)) # add data, a float value between 10-50 with 1 decimal 
print("All items past 24 hours:")
test = get_24hours(2)
for row in test:
    print(row)
print("New database item added, all good homie.")
#==================================================
# Print after something

if __debug__:
    with conn:
        data = conn.execute("SELECT * FROM PATIENT_STATS")
        #data = conn.execute("SELECT * FROM PATIENT_STATS WHERE measurement_ml >= 23")
        print("\n\nafter:")
        for row in data:
            print(row)
#==================================================


conn.close() # close connection with database
