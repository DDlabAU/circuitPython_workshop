import time
from adafruit_circuitplayground import cp   # enable onboard hardware (e.g. pixels)
import board                                # enable general purpose pins
import digitalio                            # to set pins as DIGITAL input and output

## variables
pin = board.A1                          #pin Signal-wire is attached to

## enable external button
button = digitalio.DigitalInOut(pin)    # name pin "button" and set pin as a digital input/output
button.switch_to_input()                # make pin input


while True:
    print("Button value:", button.value)
    # the button reads True when not pressed and False when pressed

    if not button.value:  # button is pushed
        cp.pixels.fill((0, 100, 255))
        cp.play_file("dip.wav")

    else:
        cp.pixels.fill((0, 0, 0))

    time.sleep(0.01)

