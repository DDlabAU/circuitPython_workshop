# Flask server for serving Circuit Playground Express sensor data
# This server reads temperature and humidity readings from a SQLite database
# and provides them via REST API endpoints.

#obs this a rough creation using Ai meant as an example. 

from flask import Flask, jsonify
import sqlite3
import os

# Create Flask application
app = Flask(__name__)

# --- Database Configuration ---
# Path to the SQLite database file (shared with logData.py in onComputer)
db_path = os.path.join(os.path.dirname(__file__), '..', 'onComputer', 'cpx_data.db')

# Function to get database connection
# check_same_thread=False allows reading while logData.py is writing
def get_connection():
    return sqlite3.connect(db_path, check_same_thread=False)

# --- API Endpoints ---

# GET /readings/<n> - Returns last n sensor readings as JSON
# Example: /readings/5 returns the 5 most recent readings
@app.route("/readings/<int:n>", methods=["GET"])
def get_readings(n):
    conn = get_connection()
    cursor = conn.cursor()
    # Get the last n readings, ordered by most recent first
    cursor.execute("SELECT timestamp, temperature, humidity FROM readings ORDER BY id DESC LIMIT ?", (n,))
    rows = cursor.fetchall()
    conn.close()
    # Reverse to show in chronological order (oldest first)
    rows.reverse()
    # Convert to list of dictionaries for JSON response
    data = [{"timestamp": r[0], "temperature": r[1], "humidity": r[2]} for r in rows]
    return jsonify(data)

# GET / - Returns server information and available endpoints
@app.route("/")
def index():
    return jsonify({
        "message": "Sensor data server is running",
        "endpoints": ["/readings/<n>", "/view"]
    })

# GET /view - Returns an HTML page displaying the last 10 readings in a table
@app.route("/view")
def view():
    conn = get_connection()
    cursor = conn.cursor()
    # Get last 10 readings
    cursor.execute("SELECT timestamp, temperature, humidity FROM readings ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    rows.reverse()  # chronological order

    # Build HTML table
    html = """
    <html>
    <head><title>Sensor Data Dashboard</title></head>
    <body>
    <h1>Circuit Playground Express Sensor Readings</h1>
    <p>Last 10 readings from the database</p>
    <table border="1">
    <tr><th>Timestamp</th><th>Temperature (°C)</th><th>Humidity (%)</th></tr>
    """
    for row in rows:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    html += """
    </table>
    <p><a href="/">Back to API info</a></p>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    # host="0.0.0.0" gør serveren tilgængelig fra andre computere på netværket
    app.run(host="0.0.0.0", port=5000)