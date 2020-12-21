# -*- coding: utf-8 -*-
# This the the code for contineous excitation for 30 min

# Key commands to control de Duinos
# openJIP > Use MF to measure fluoresnece
# UNO     > Use PDC to trigger photodamage 

# Dependencies
import serial
import time
import csv
import datetime
from time import strftime
print("Dependencies imported")

# COM ports and devices
print("Calling COM ports")
aUNO    = serial.Serial('COM6', 9600) # This is the Arduino UNO acting as a light trigger
openJIP = serial.Serial('COM7', 115200) # set the comport
print("Comports available")

#ser.flush() # cleans bus
#time.sleep(1) # allow time to clear request
#ser.write(b'MF') # send command to the Open-JIP to do a command based on Harvey's code

# Commands to Open JIP
def measure_fluorescence():
    global time_stamps, values
    openJIP.flush()      # Cleans Bus that a device is connected to syntax is {device}.flush()
    time.sleep(1)
    openJIP.write(b'MF') # Sends an instruction to a device conected, the syntax is {device}.write(b'{COMMAND}')
    time_stamps = []
    values = []
    for _ in range(2000):
        fluorescence_bytes = openJIP.readline()
        decoded_fluorescence_bytes = str(fluorescence_bytes[0:len(fluorescence_bytes) - 2].decode("utf-8"))
        data_split = [float(s) for s in decoded_fluorescence_bytes.split("\t")]
        x_data = data_split[0]
        y_data = float(data_split[1])
        # print(x_data, y_data) # print to test is transfering to PC data
        time_stamps.append(x_data) # Save to array
        values.append(y_data) # Save to array

def upload(): # This records and logs the curve into a csv file
    global day_night
    worksheet_name = "Open-JIP Data.csv"
    with open(worksheet_name, 'a') as f:
        try:
            writer = csv.writer(f)
            spreadsheet_time = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            writer.writerow([spreadsheet_time, time_stamps, values])
            print("Written to local csv")

        except:
            print("Failed to write to local csv file...")
    f.close()

# Commands to UNO
    
def photodamage():
    aUNO.flush()
    time.sleep(0.05)
    aUNO.write(b'PDC')
    print ('photodamaging')
    task = aUNO.readline(10) # Read the "Done" command from the arduino (10 second timeout but it should be almost instantaneous depending on the baudrate and the size of your trigger() command)
    #task.readline(10)
    task = str(task[0:len(task)-2].decode("utf-8"))
    if(task == "Done"):
        print ('photodamaged')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Routine
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

print ('Measurement initiated')
no_cycles = 2


for i in range (0, no_cycles): # Loop and repeat this sequence for 10 cycles
    print ('This is the cycle', i, 'of ', no_cycles)
    print (datetime.datetime.now())
    measure_fluorescence()
    upload()
    time.sleep(2) # Wait 2 s to restart photodamage
    photodamage()
        
    
openJIP.close()
aUNO.close()