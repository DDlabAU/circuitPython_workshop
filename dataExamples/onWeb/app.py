from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'cpx_data.db')

def get_latest_reading():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT timestamp, temperature, humidity
            FROM readings
            ORDER BY id DESC
            LIMIT 1
        """)

        row = cursor.fetchone()
        conn.close()

        if row:
            return {"timestamp": row[0], "temperature": row[1], "humidity": row[2]}
        else:
            return None
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    data = get_latest_reading()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)