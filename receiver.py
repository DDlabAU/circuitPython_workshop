import serial
import os
import serial.tools.list_ports
import sqlite3
from datetime import datetime
import time

# --- Auto-detect CPX serial port ---
def find_cpx_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Adafruit CPX vendor ID is 0x239A
        if port.vid == 0x239A:
            return port.device
    return None

port = find_cpx_port()
if port is None:
    print("Could not find CPX! Make sure it is plugged in.")
    exit()

print(f"Found CPX on port: {port}")

# --- Set up SQLite database ---
db_path = os.path.abspath(os.path.join('web', 'cpx_data.db'))
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        tvoc INTEGER,
        eco2 INTEGER,
        button_count INTEGER
    )
''')
conn.commit()

# --- Listen to serial and save data ---
ser = serial.Serial(port, 115200, timeout=1)
print("Listening for data... press CTRL+C to stop")

last_save = time.monotonic()  # track last database insert

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if ',' in line:
            now = time.monotonic()
            # Only parse & save once per second
            if now - last_save >= 1.0:
                try:
                    tvoc, eco2, button_count = line.split(',')
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    cursor.execute(
                        "INSERT INTO readings VALUES (NULL, ?, ?, ?, ?)",
                        (timestamp, int(tvoc), int(eco2), int(button_count))
                    )
                    conn.commit()
                    print(f"{timestamp} | TVOC: {tvoc} | eCO2: {eco2} | Button presses: {button_count}")
                    last_save = now
                except Exception as e:
                    print(f"Ignored malformed line: {line} ({e})")

except KeyboardInterrupt:
    print("Stopped!")
    ser.close()
    conn.close()