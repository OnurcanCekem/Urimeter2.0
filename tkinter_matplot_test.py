# Testing tkinter with database
import sys
sys.path
# matplotlib imports
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

# database imports
import sqlite3
from sqlite3 import Error, Timestamp
from time import gmtime, strftime
conn = None # Variable to use as connection with the database

# test imports
import matplotlib.pyplot as plt
import datetime as dt

"""
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.plot(x,y)
plt.gcf().autofmt_xdate()
plt.show()
"""

root = tk.Tk() # create tkinter window
root.wm_title("Embedding in Tk") # tkinter window title

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


def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

conn = sqlite3.connect(r"db_test.db") # Connect to the database
# ==============================================================
data_base = get_24hours(2) # all database variables that are relevant for id = 2
x = [] # x-axis data for graph
y = [] # y-axis data for graph

import time # import time
for row in data_base:
    Timestamp_db = row[3] # index 3 = timestamp
    Timestamp_converted = dt.datetime.strptime(Timestamp_db,"%Y-%m-%d %H:%M:%S") # Convert datetime to custom format, else it's not equal to datetime from xlimit for unknown reasons (data type?)
    x.append(Timestamp_converted) # add timestamp
    y.append(row[4]) # add volume ; index 4 = volume (ml)
    
    #debug prints
    #print(row) # print all elements in row
    #print(str(row[3]) + " and " + str(row[4])) # print only 'timestamp' and 'measurement'


#debug print all values in x and y
print("\nx vals: ")
for value in x:
    print(value)

print("\nY vals: ")
for value in y:
    print(value)


# example values for testing
# code to randomly generate values for the past day
#import random
#x = [dt.datetime.now() - dt.timedelta(minutes=i) for i in range(24)] # original one
#y = [i+random.gauss(0,1) for i,_ in enumerate(x)]

# create plot in Tkinter
f = Figure(figsize=(10,5), dpi=100)
graph = f.add_subplot()

# graph settings
graph.set_title('Metingen afgelopen 24 uur') # set title for graph
graph.set_ylabel('volume (ml)') # set label for y-axis
graph.set_xlabel('Tijd (maand-dag uur)') # set label for x-axis
graph.set_ylim([0, 50]) # set y-limit to up to 50 ml
graph.grid(True)

# calculate time for limit
time_max = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
time_min = dt.datetime.now() - dt.timedelta(hours=24)
time_min_converted = time_min.strftime("%Y-%m-%d %H:%M:%S") # Convert datetime to custom format
print("Time_min: " + time_min_converted)

graph.set_xlim([dt.datetime.now() - dt.timedelta(hours=24), dt.datetime.now()]) # set x-limit to up to 24 hours
#a.set_xlim([dt.datetime.now() - dt.timedelta(minutes=24), dt.datetime.now()]) # uncomment for 24 minutes version

# Start plotting
graph.plot(x,y)
canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

canvas.mpl_connect("key_press_event", on_key_press)

button = tk.Button(master=root, text="Quit", command=_quit)
button.pack(side=tk.BOTTOM)
tk.mainloop()


# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
# ==============================================================
conn.close() # close connection with database

# junk code
"""
# Single line in one canvas
f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

canvas.mpl_connect("key_press_event", on_key_press)

button = tk.Button(master=root, text="Quit", command=_quit)
button.pack(side=tk.BOTTOM)
matplotlib.pyplot.plot_date(dates, y_values)
tk.mainloop()
"""

# plot in Matplotlib
"""
import random
# make up some data
x = [dt.datetime.now() + dt.timedelta(hours=i) for i in range(24)]
y = [i+random.gauss(0,1) for i,_ in enumerate(x)]

# plot
plt.scatter(x,y)
# beautify the x-labels
plt.gcf().autofmt_xdate()

plt.show()
plt.plot_date(x, y)
"""