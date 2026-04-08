import time
import board                                # enable general purpose pins
import busio                                # enable I2C communication
import digitalio                            # to set pins as DIGITAL input and output
from adafruit_circuitplayground import cp   # enable onboard hardware (e.g. buttonA)
import adafruit_sgp30


## variables
buttonPin = board.A1                        # change according to setup
button_count = 0
last_button_state = False
last_send = time.monotonic()                # timer for printing data


## setup I2C pins for SGP30 sensor
i2c = busio.I2C(board.A4, board.A5)         # I2C on A4 (SDA) and A5 (SCL)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)  # create sensor object
sgp30.iaq_init()                            # initialize sensor

## setup external button
button = digitalio.DigitalInOut(buttonPin)  # name pin button and set pin as digital input/output
button.switch_to_input()                    # make pin input



while True:
    if cp.button_a:                     # if onboard button A pressed
        button_count = 0                # reset button count

    pressed = not button.value          # read external button (False when pressed)


    if pressed and not last_button_state:
        button_count += 1
    last_button_state = pressed

    #get sensor readings
    tvoc = sgp30.TVOC
    eco2 = sgp30.eCO2

    now = time.monotonic()              # gets current time

    if now - last_send >= 1.0:          # send to computer every 1 second
        print(f"{tvoc},{eco2},{button_count}")
        last_send = now                 # reset timer

    time.sleep(0.05)                  # Write your code here :-)
