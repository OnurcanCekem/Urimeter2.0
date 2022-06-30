"""
 * Urimeter2.0.py
 *
 *  Created on: June 28, 2022
 *  Last update: June 29, 2022
 *      Author: onurc
 *  Description: Full program of the Urimeter 2.0 project. This program is the combined version of all individual parts used in this project.
                 Makes use of: tkinter with matplotlib, sqlite database, time hourlymeasure and potentially a keypad.
                 If you want to understand the code, I suggest reading animate function.
                 Change interval time 
 """

#==================
#  Matplotlib imports
import sys
import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import datetime as dt

from matplotlib.ticker import MultipleLocator, FormatStrFormatter # required for formatting dates (grid)
import matplotlib.dates as mdates # required for formatting dates
import random # required for generating data
#==================
# database imports
import sqlite3
from sqlite3 import Error, Timestamp
import time # required for localtime
from time import gmtime, strftime # gmtime, the darkest pit of hell has opened to swallow you whole so don't keep the devil waiting for being 2 hours behind and wasting 2 of mine.
                                  # Solved with time.localtime().
# unused
import numpy as np

sys.path
conn = None # Variable to use as connection with the database
"""
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.plot(x,y)
plt.gcf().autofmt_xdate()
plt.show()
"""

root = tk.Tk() # create tkinter window
root.geometry("800x480") # windows size, 800x480 is the Raspberry Pi's display size
root.wm_title("Lijn grafiek") # tkinter window title

# Add data to database
# Parameter Patient_ID: The ID of a patient
# Parameter name: The name of a patient
# Parameter Measurement_ML: The current measured urine
def add_data(Patient_ID, name, Measurement_ML):
    #data_add = (Patient_ID, name, strftime("%Y-%m-%d %H:%M:%S", gmtime()), Measurement_ML) # create case to store data
    data_add = (Patient_ID, name, strftime("%Y-%m-%d %H:%M:%S", time.localtime()), Measurement_ML)
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

# Get the most recent insert from the database.
def get_Latest():
    data = conn.execute("SELECT * FROM PATIENT_STATS WHERE ID=(SELECT MAX(ID) FROM PATIENT_STATS)") # retrieve all rows with Patient_ID
    return data

# Get all measurements in the past 24 hours from given Patient ID.
# Parameter Patient_ID: The ID of a patient
def get_24hours(Patient_ID):
    data = conn.execute("SELECT * FROM PATIENT_STATS WHERE Timestamp > datetime('now', '-1 day') AND Patient_ID=?", (Patient_ID,)) # retrieve all rows in the past 24hrs with Patient_ID
    return data

# Copied, not my function.
def on_key_press(event):
    print("you pressed {}".format(event.key))
    # key_press_handler(event, canvas, toolbar)

# The quit button
def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

conn = sqlite3.connect(r"db_test.db") # Connect to the database
start_data_flag = 0 # flag to keep track for adding data in animate. No touchie.

# ==============================================================
# Variables
# ==============================================================
intervaltime = 2000 # time in ms for each interval. 2000 = 2 seconds
debug = 0; # 0 for 24hours, 1 for 24 minutes, 2 for 24 seconds
above_set_value = 40 # upper end of set value
below_set_value = 20 # lower end of set value
above_set_value_color = 'red' # color text when above set value
below_set_value_color = 'red' # color text when below set value


# ==============================================================
# Start of actual program
# ==============================================================
# This code below is kind of redundant, as it should be in a function.
# I'm creating the plot now and in animate.
# Get data points from database
data_base = get_24hours(2) # all database variables that are relevant for id = 2
x = [] # x-axis data for graph
y = [] # y-axis data for graph

# Store data points in x-axis and y-axis
for row in data_base:
    Timestamp_db = row[3] # index 3 = timestamp
    Timestamp_converted = dt.datetime.strptime(Timestamp_db,"%Y-%m-%d %H:%M:%S") # Convert datetime to custom format, else it's not equal to datetime from xlimit for unknown reasons (data type?)
    x.append(Timestamp_converted) # add timestamp
    y.append(row[4]) # add volume ; index 4 = volume (ml)
    
    

# create plot in Tkinter
f = plt.figure(figsize=(10,5), dpi=100)
graph = f.add_subplot()

# Start plotting
graph.plot(x,y, 'bo-') # 'bo-' means blue color, round points, solid lines


# Data labels
for x,y in zip(x,y):
    label = "{:.1f}".format(y) # 1 decimal
    graph.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,5), # distance from text to points (x,y)
                 ha='center') # horizontal alignment can be left, right or center


button = tk.Button(master=root, text="Quit", command=_quit)
button.pack(side=tk.BOTTOM)

# If a certain time has passed
from matplotlib.animation import FuncAnimation

# The animate function, called by FuncAnimation(plt.gcf(), animate, interval=2000)
# Parameters: i - Has to be here for some reason. First 2 times when animate is called i = 0, then it's a counter.
# Description: The graph is cleared first, second is create and store new data, third is recreate graph
#              Recreating the graph is achieved by plotting data, Adding grid and annotations

def animate(i):
    graph.clear() # Clear the graph, or everything gets doubled and eventually lags out.
    
    # ==============================================================
    #  Adding new data
    # ==============================================================
    # Go through animate twice without adding data.
    # 1. Manually call animate to create it.
    # 2. For some reason i is 0 for the first 2 animates even though the 2nd animate waits for interval
    #    To solve this I created a flag.
    
    global start_data_flag # Grab global flag to keep track
    if start_data_flag != 2: # No need to add data
        start_data_flag += 1 # Add up
    else: # Now we start adding data
        add_data(2, 'Jesse', round(random.uniform(15,50),1)) # create data, 1 decimal float value between 15-50
    
    xs = [] # storage x-axis
    ys = [] # storage x-axis
    data = get_24hours(2) # storage from database, get dataset from past 24 hours of Patient_ID "2"
    for row in data: # loop through all data from the past 24 hours
        Timestamp_db = row[3] # index 3 = timestamp
        Timestamp_converted = dt.datetime.strptime(Timestamp_db,"%Y-%m-%d %H:%M:%S") # Convert datetime to custom format, else it's not equal to datetime from xlimit for unknown reasons (data type?)
        xs.append(Timestamp_converted) # add timestamp
        ys.append(row[4]) # add volume; index 4 = volume (ml)
    with conn: # Establish connection. This is needed or the added data won't save in database.
        data = conn.execute("SELECT * FROM PATIENT_STATS")
    
    # debug output, feel free to disable
    latest = get_Latest()
    for row in latest:
        print("Recent addition:")
        print(row)
    # ==============================================================
    #  End of adding data
    # ==============================================================
    
    # ==============================================================
    # graph settings (datetime)
    # ==============================================================
    # Set the x-axis by using datetime
    
    if debug == 0: # 24 hours
        graph.set_xlim([dt.datetime.now() - dt.timedelta(hours=24), dt.datetime.now()]) # update locator to hours

    if debug == 1: # 24 minutes
        graph.set_xlim([dt.datetime.now() - dt.timedelta(minutes=24), dt.datetime.now()]) # update locator to minutes
    
    elif debug == 2: # 24 seconds
        graph.set_xlim([dt.datetime.now() - dt.timedelta(seconds=24), dt.datetime.now()]) # update locator to seconds
    
    # ==============================================================
    # End of graph settings datetime
    # ==============================================================
    
    # ==============================================================
    # graph settings (labels, grid)
    # ==============================================================
    # 24 hour version
    if debug == 0:
        graph.set_title('Metingen afgelopen 24 uur') # set title for graph
        graph.set_xlabel('Tijd (dag-uur)') # set label for x-axis
        graph.set_xlim([dt.datetime.now() - dt.timedelta(hours=24), dt.datetime.now()]) # set x-limit to up to 24 hours
        graph.xaxis.set_minor_locator(MultipleLocator(1/24)) # minor line each hour
        graph.xaxis.set_major_formatter(mdates.DateFormatter("%d-%H")) # recognize grid in date
        
    # 24 minutes version
    if debug == 1: 
        graph.set_title('Metingen afgelopen 24 minuten') # set title for graph
        graph.set_xlabel('Tijd (uur en minuten)') # x-axis label 
        graph.set_xlim([dt.datetime.now() - dt.timedelta(minutes=24), dt.datetime.now()]) # 24-minute version
        graph.xaxis.set_minor_locator(MultipleLocator(1/(24*60))) # minor line each minute
        graph.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M")) # date format
    # 24 seconds version
    elif debug == 2: 
        graph.set_title('Metingen afgelopen 24 seconden') # set title for graph
        graph.set_xlabel('Tijd [minuut en seconden]') # x-axis label 
        graph.set_xlim([dt.datetime.now() - dt.timedelta(seconds=24), dt.datetime.now()]) # 24-minute version
        graph.xaxis.set_minor_locator(MultipleLocator(1/(24*60*60))) # minor line each minute
        graph.xaxis.set_major_formatter(mdates.DateFormatter("%M:%S")) # date format
    
    graph.set_ylabel('volume [ml]') # set label for y-axis
    graph.set_ylim([0, 50]) # set y-limit to up to 50 ml
    graph.yaxis.set_major_locator(MultipleLocator(10)) # each 10 ml major line
    graph.yaxis.set_minor_locator(MultipleLocator(2)) # each 2 ml minor line
    graph.xaxis.grid(True,'minor',linewidth=0.5) # enable x-axis minor line
    graph.yaxis.grid(True,'minor',linewidth=0.5) # enable y-axis minor line
    graph.xaxis.grid(True,'major',linewidth=2) # enable x-axis major line
    graph.yaxis.grid(True,'major',linewidth=2) # enable y-axis major line
    # ==============================================================
    #  End of graph settings
    # ==============================================================
    
    # ==============================================================
    #  Annotation settings (text)
    # ==============================================================
    # Annotation, which is text above each position in the plot
    annotate_colour = ''
    for x,y in zip(xs,ys): # loop through all xs and ys values
        label = "{:.1f}".format(y) # 1 decimal
        if y > above_set_value: # if above set value
            annotate_colour = above_set_value_color
        elif y < below_set_value: # if below set value
            annotate_colour = below_set_value_color
        else: # otherwise, it's good
            annotate_colour = 'black'
        graph.annotate(label, # this is the text
                 (x,y), # these are the coordinates to position the label
                 textcoords="offset points", # how to position the text
                 xytext=(0,5), # distance from text to points (x,y)
                 ha='center',
                 color = annotate_colour) # horizontal alignment can be left, right or center
    # ==============================================================
    #  End of graph settings
    # ==============================================================
    # Start plotting.
    # For more details on colors/pyplot commands visit: https://matplotlib.org/2.1.2/api/_as_gen/matplotlib.pyplot.plot.html
    graph.plot(xs,ys, 'bo-')# 'bo-' means blue color, round points, solid lines
    # ==============================================================    
    # End of animate
    
# Haven't really bothered to check this.
canvas = FigureCanvasTkAgg(f, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
canvas.mpl_connect("key_press_event", on_key_press)

# Start triggering a function each interval (ms)
ani = FuncAnimation(plt.gcf(), # Get current figure
                    animate, # Call the function "animate"
                    interval=intervaltime) # Each 2000 ms

animate(-1) # Start animating once to get the canvas started.
root.mainloop() # LOOOOOOP

# ==============================================================
# End of program
# ==============================================================
conn.close() # close connection with database


# Junk code

# ==============================================================
# Code to debug time (datetime and time.perf_counter)
# ==============================================================
# datetime debug
#time_max = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#time_min = dt.datetime.now() - dt.timedelta(hours=24)
#time_min_converted = time_min.strftime("%Y-%m-%d %H:%M:%S") # Convert datetime to custom format
#print("Time_min: " + time_min_converted)

# time.perf_counter debug
#starttime = int(time.perf_counter_ns() / 1000000000) # start time of program
#print(starttime)
#print(strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# ==============================================================

# ==============================================================
# timedelta
# ==============================================================
# code to randomly generate values for the past 24 minutes
# dt.timedelta(hours=i)  for 24 hours
# dt.timedelta(minutes=i) for 24 minutes
# dt.timedelta(seconds=i) for 24 seconds
# ==============================================================

# ==============================================================
# Generating random data 
# ==============================================================
# import random
# x = [dt.datetime.now() - dt.timedelta(minutes=i) for i in range(24)] # original one
# y = [i+random.gauss(0,1) for i,_ in enumerate(x)]
# ==============================================================

# ==============================================================
# code for changing color depending on set value
# ==============================================================
# index = 0
# for y in ys:
#     xpos = xs[index]
#     index += 1
#     if y > 40: # if above set value
#         graph.plot(xpos,y, 'ro-') # 'ro-' means red color, round points, solid lines
#     elif y < 20: # if below set value
#         graph.plot(xpos,y, 'ro-') # 'ro-' means red color, round points, solid lines
#     else: # otherwise it's good
#         graph.plot(xpos,y, 'bo-') # 'bo-' means blue color, round points, solid lines
# ==============================================================

# ==============================================================
# Toolbar
# ==============================================================
# Generates errors for some reason as the program runs, besides I'm not really using this
# toolbar = NavigationToolbar2Tk(canvas, root)
# toolbar.update()
# canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
# ==============================================================

# ==============================================================
# Debug prints
# ==============================================================
# database values
# print(row) # print all elements in row
# print(str(row[3]) + " and " + str(row[4])) # print only 'timestamp' and 'measurement'

# debug print all values in x and y
# print("\nx vals: ")
# for value in x:
#     print(value)

# print("\nY vals: ")
# for value in y:
#     print(value)
# ==============================================================

