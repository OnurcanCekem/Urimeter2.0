"""
 * tkinter_keypad_database.py
 *
 *  Created on: June, 2022
 *  Last update: June 27, 2022
 *      Author: onurc
 *  Description: Tkinter test program for keypad to test the lambda function.
 """



# Keypad imports
from tkinter import *
import tkinter

# Sqlite imports
import sqlite3
import random # for RNGesus

from sqlite3 import Error
from time import gmtime, strftime
import datetime
conn = None # Variable to use as connection with the database

#===============================================================
# Database
#===============================================================
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

# Get all measurements in the past 24 hours from given Patient ID.
# Parameter Patient_ID: The ID of a patient
def get_24hours(Patient_ID):
    data = conn.execute("SELECT * FROM PATIENT_STATS WHERE Timestamp > datetime('now', '-1 day') AND Patient_ID=?", (Patient_ID,)) # retrieve all rows in the past 24hrs with Patient_ID
    return data

conn = sqlite3.connect(r"db_test.db") # Connect to the database

#add_data(2, 'Jesse', 29.5)

#Print before something
if __debug__:
    with conn:
        data = conn.execute("SELECT * FROM PATIENT_STATS")
        print("before:")
        for row in data:
            print(row)
        print("\n")
#===============================================================
# Keypad
#===============================================================

root = Tk()
root.geometry("800x480") # windows grootte 

# Show input
input_label = tkinter.Label(root, text="Meting [ml]:")
input_label.grid(column=0, row=0, sticky=tkinter.W, padx=5, pady=5)
input_entry = tkinter.Entry(root)
input_entry.grid(column=1, row=0, sticky=tkinter.E, padx=5, pady=5)

index = 0
create_connection(r"db_test.db") # Creates connection to database. Creates a new database file if file does not exist.

def buttonPressed(button):
    global index
    #print("Hello there button " + str(button))
    print("index: " + str(index))

    # Keypad 1-9
    if(button >= 1) and (button <= 9):
        print("Keypad 1")
        input_entry.insert(index,str(button))
        index = index + 1
    
    elif(button == 10):
        print(".")
        input_entry.insert(index,".")
        index = index + 1
    
    # Clear button
    elif(button == 11):
        index = index - 1
        input_entry.delete(index)
        if(index < 0):
            index = 0
    
    # Add data to database button
    elif(button == 12):
        print("add data value: " + input_entry.get())
        print("add data value: " + str(float(input_entry.get())))
        # add the data to database
        data = "{:.1f}".format(float(input_entry.get()))
        add_data(2, 'Jesse', data) # add data, a float value between 10-50 with 1 decimal 
        #add_data(2, 'Jesse', round(random.uniform(15,50),1)) # add data, a float value between 10-50 with 1 decimal 
        with conn:
            data = conn.execute("SELECT * FROM PATIENT_STATS")
        for i in range(0,index): # clear selection
            input_entry.delete(0)
        index = 0

    # Delete last data from database button
    elif(button == 13):
        print("delete, IDK")
        delete_Latest()

root.title("Keypad")
btn1=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(1), text='1').grid(row=4,column=0)
btn2=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(2), text='2').grid(row=4,column=1)
btn3=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(3), text='3').grid(row=4,column=2)
btn4=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(4), text='4').grid(row=3,column=0)
btn5=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(5), text='5').grid(row=3,column=1)
btn6=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(6), text='6').grid(row=3,column=2)
btn7=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(7), text='7').grid(row=2,column=0)
btn8=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(8), text='8').grid(row=2,column=1)
btn9=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(9), text='9').grid(row=2,column=2)
btn9=Button(root,padx=8,pady=8,bd=5,bg='white',fg='blue',font=('times new rmoan',30,'bold'),command=lambda: buttonPressed(10), text='.').grid(row=4,column=4)

delete_btn =Button(root,padx=8,pady=15,bd=5,bg='white',fg='blue',font=('times new rmoan',20,'bold'),command=lambda: buttonPressed(11), text='clear karakter').grid(row=2,column=4)
adddata_btn=Button(root,padx=8,pady=15,bd=5,bg='green',fg='blue',font=('times new rmoan',15,'bold'),command=lambda: buttonPressed(12), text='toevoegen invoer data').grid(row=1,column=4)
deletedata_btn =Button(root,padx=8,pady=15,bd=5,bg='red',fg='blue',font=('times new rmoan',12,'bold'),command=lambda: buttonPressed(13), text='verwijder laatste data').grid(row=0,column=4)
destroy_btn = Button(root,padx=8,pady=15,bd=5,bg='white',fg='blue',font=('times new rmoan',12,'bold'),command=lambda: root.destroy(), text='Schakel naar grafiek').grid(row=4,column=5)
root.mainloop()
conn.close() # close connection with database

