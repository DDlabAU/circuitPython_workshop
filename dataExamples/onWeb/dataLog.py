import time
import board
import busio
from adafruit_circuitplayground import cp
import adafruit_ahtx0
import sqlite3
import os
from datetime import datetime

# --- I2C Setup ---
i2c = busio.I2C(board.A4, board.A5)
aht20 = adafruit_ahtx0.AHTx0(i2c)

# --- Database Setup ---
db_path = os.path.join(os.path.dirname(__file__), 'cpx_data.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        temperature REAL,
        humidity REAL
    )
''')
conn.commit()

print("Logging CPX data... Press CTRL+C to stop")

try:
    while True:
        temperature = aht20.temperature
        humidity = aht20.relative_humidity

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute(
            "INSERT INTO readings VALUES (NULL, ?, ?, ?)",
            (timestamp, temperature, humidity)
        )
        conn.commit()

        print(f"{timestamp} | Temp: {temperature:.2f}°C | Humidity: {humidity:.2f}%")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped logging.")
    conn.close()