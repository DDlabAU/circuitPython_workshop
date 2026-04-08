import time
import board
import busio
from adafruit_circuitplayground import cp
import adafruit_ahtx0

# --- I2C via A4 (SCL) and A5 (SDA) ---
i2c = busio.I2C(board.A4, board.A5)
aht20 = adafruit_ahtx0.AHTx0(i2c)

while True:
    temperature = aht20.temperature
    humidity = aht20.relative_humidity

    print(f"{temperature:.2f},{humidity:.2f}")

    time.sleep(1)




