#obs this a rough creation using Ai meant as an example. 

import serial                       # lets python talk to serial ports (USB)
import serial.tools.list_ports     # lets us list all available serial ports
import sqlite3                     # lets us work with a sqlite database
import os                          # lets us work with file paths
from datetime import datetime      # lets us get the current date and time
import time                        # lets us track time


# --- Find the CPX automatically ---
# this function loops through all USB ports on the computer
# and returns the one that belongs to an Adafruit board
def find_cpx_port():
    # get a list of all connected serial devices
    all_ports = serial.tools.list_ports.comports()

    for port in all_ports:
        # 0x239A is the unique vendor ID for all Adafruit boards
        # this is how we know which port is the CPX
        if port.vid == 0x239A:
            return port.device  # return the port name e.g. COM19

    # if we get here, no Adafruit board was found
    return None


# --- Try to find the CPX ---
port = find_cpx_port()

if port is None:
    print("Could not find CPX! Make sure it is plugged in.")
    exit()  # stop the script if no CPX is found

print(f"Found CPX on port: {port}")


# --- Set up the database ---
# build the path to the database file
# __file__ is the path to this script
# we save the database in the same folder as this script
db_path = os.path.join(os.path.dirname(__file__), 'cpx_data.db')

# connect to the database (creates the file if it doesn't exist)
connection = sqlite3.connect(db_path)

# a cursor lets us run SQL commands on the database
cursor = connection.cursor()

# create the table if it doesn't already exist
# each row will have: an id, a timestamp, temperature and humidity
cursor.execute('''
    CREATE TABLE IF NOT EXISTS readings (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp   TEXT,
        temperature REAL,
        humidity    REAL
    )
''')

# save the changes to the database
connection.commit()


# --- Open the serial connection to the CPX ---
# 115200 is the baud rate - the speed of the connection
# timeout=1 means we wait max 1 second for data before moving on
serial_connection = serial.Serial(port, 115200, timeout=1)

print("Listening for data... press CTRL+C to stop")


# --- Keep track of when we last saved ---
# we use this to make sure we only save once per second
last_save_time = time.monotonic()


# --- Main loop ---
try:
    while True:

        # read one line from the CPX over USB serial
        # decode converts it from bytes to a normal string
        # strip removes any whitespace or newlines at the end
        raw_line = serial_connection.readline().decode('utf-8').strip()

        # only process the line if it contains a comma
        # this filters out any debug messages or empty lines
        if ',' in raw_line:

            # check how much time has passed since last save
            current_time = time.monotonic()
            time_since_last_save = current_time - last_save_time

            # only save to database once per second
            if time_since_last_save >= 1.0:

                try:
                    # split the line into two values at the comma
                    # e.g. "23.45,67.89" becomes ["23.45", "67.89"]
                    temperature, humidity = raw_line.split(',')

                    # get the current date and time as a string
                    # e.g. "2024-01-01 12:00:01"
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    # insert the data into the database
                    cursor.execute(
                        "INSERT INTO readings VALUES (NULL, ?, ?, ?)",
                        (timestamp, float(temperature), float(humidity))
                    )

                    # save the changes to the database
                    connection.commit()

                    # print the data to the terminal so we can see it
                    print(f"{timestamp} | Temp: {temperature}°C | Humidity: {humidity}%")

                    # update the last save time
                    last_save_time = current_time

                except Exception as error:
                    # if something goes wrong, print the error and keep going
                    print(f"Ignored malformed line: {raw_line} ({error})")

# --- Stop cleanly when CTRL+C is pressed ---
except KeyboardInterrupt:
    print("Stopped!")
    serial_connection.close()   # close the serial connection
    connection.close()          # close the database connection