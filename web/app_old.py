import os
import sqlite3
from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='templates')

# --------------------------
# Database helper
# --------------------------
def get_db():
    db_path = os.path.join(os.path.dirname(__file__), 'cpx_data.db')

    # create DB and table if it doesn't exist
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        conn.execute('''
            CREATE TABLE readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                tvoc INTEGER,
                eco2 INTEGER,
                button_count INTEGER
            )
        ''')
        # insert dummy row so page shows something
        conn.execute('''
            INSERT INTO readings (timestamp, tvoc, eco2, button_count)
            VALUES (datetime('now'), 50, 400, 0)
        ''')
        conn.commit()
        conn.close()

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# --------------------------
# Routes
# --------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def api_data():
    conn = get_db()
    latest = conn.execute('''
        SELECT * FROM readings
        ORDER BY timestamp DESC
        LIMIT 1
    ''').fetchone()
    conn.close()

    return jsonify({
        'reading': dict(latest) if latest else None,
        'button_count': latest['button_count'] if latest else 0
    })


# --------------------------
# Main
# --------------------------
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)