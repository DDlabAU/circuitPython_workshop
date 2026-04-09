## Examples of how to save data from Circuit Playgroudn Express and the sensor AHT20

This folder contains three examples on how to log data from a sensor.

# `lib` folder
Contains the necessary libraries for the CIRCUITPY drive. Place in `lib` folder on Circuit Playground Express.

# examples -------------------------------------------

## `OnBoard`
Follows the example made by Lady Ada and Kattni Rembor, with examples changed to work on CPX.
https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-storage

## `onComputer`
Logs sensor data from CPX to a SQLite database on the computer via serial connection.
- `code.py`: Runs on CPX to send sensor readings
- `logData.py`: Runs on computer to receive data and save to database

## `onWeb`
Serves the logged sensor data via a Flask web API.
- `flask_server.py`: Web server that provides REST endpoints to access the data
contains firmware for CPX and a python script. It created a db files with the data. 


cody.py should be placed on the CIRCUITPY(D:) drive 
- remember to add the libraries from the lib folder too if not already on the CIRCUITPY(D:) 

# software
You need python on your computer: https://www.python.org/downloads/ 
and then install pyserial

# acces data 
For the onComputer example, I use the DBbrowser program to display the db file: https://sqlitebrowser.org/. 
You don't need this program but I find i helpful. 

# usage 
navigate to the onComputer folder
run the script 

python logData.py 

# stopping the program 
press CTRL + C to stop

--------

## onWeb

contains a script for a flask werserver
Remeber, you must run the logData.py file in the onComputer example to generate a database for flask to use 


# usage 
navigate to the onWeb folder
run the script 

python flask_server.py 

# stopping the program 
press CTRL + C to stop


# see data
When going to the webpage you will see something like this: 

{"endpoints":["/readings/<n>","/view"],"message":"Sensor data server is running"}

this means that you can at either add /readings/<n> or /view to you url to see the data. 
- reading<n> gives the last n readings in JSOn format
- view returns a HTML page 





