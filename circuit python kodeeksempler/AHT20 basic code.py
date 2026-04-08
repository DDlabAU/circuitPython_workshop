import time
import board
import adafruit_ahtx0

# Set up I2C and the AHT20 sensor
i2c = board.I2C()
sensor = adafruit_ahtx0.AHTx0(i2c)

while True:
    print("Temperature: %0.1f C" % sensor.temperature)
    print("Humidity:    %0.1f %%" % sensor.relative_humidity)
    print("---")
    time.sleep(2)
