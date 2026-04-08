## Examples of how to save data from Circuit Playgroudn Express and the sensor AHT20

This folder contains three examples on how to and log data from a sensor.


# lib folder 
Contains the necessary libraries for the CIRCUITPY drive. Place in lib folder on Circuit Playground Express 



# examples -------------------------------------------

## onBoard
follows the example made by lady ada and Kattni Rembor
with examples changed to work on cpx. 
https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-storage

--------

##oncomputer
contains firmware for CPX and a python script. It created a db files with the data. 


cody.py should be placed on the CIRCUITPY(D:) drive 

remember to add the libraries from the lib folder too 

# software
You need python on your computer: https://www.python.org/downloads/ 
and then install pyserial

# acces data 
I use the DBbrowser program to display the db file: https://sqlitebrowser.org/ 

# usage 
run the script 

python logData.py 

# stopping the program 
press CTRL + C to stop

--------









