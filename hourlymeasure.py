# Author: Onurcan Cekem
# V1.0 04-04-2022: Start of program, program works with in seconds and can reset.

import time # required for time of program

starttime = int(time.perf_counter_ns() / 1000000000) # start time of program
print(starttime)

time.sleep(1)



while True:
    currenttime_seconds = int(time.perf_counter_ns() / 1000000000) - starttime # Counts in seconds
    
    # If a certain time has passed
    if(currenttime_seconds == 15):
        # Do something
        print("do something, IDK")
        
        #uncomment the line below to reset the timer
        starttime = int(time.perf_counter_ns() / 1000000000) # Reset the timer
        
    print(currenttime_seconds)
    time.sleep(1)
    