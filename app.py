import sqlite3
import os
from flask import Flask, render_template

app = Flask(__name__)
DATABASE = "database/landing_page.db"




def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()

    configuracion = conn.execute(
        "SELECT * FROM configuracion_sitio LIMIT 1"
    ).fetchone()
    conn.close()
    return render_template('index.html', configuracion=configuracion)

if __name__ == '__main__':
    app.run(debug=True)