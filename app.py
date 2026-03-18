import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
DATABASE = "database/landing_page.db"




def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn



@app.route('/')
def index():
    conn = get_db_connection()
    
    # 1. Configuración
    configuracion = conn.execute("SELECT * FROM configuracion_sitio LIMIT 1").fetchone()
    
    # 2. Hero
    hero = conn.execute("SELECT * FROM hero LIMIT 1").fetchone()
    
    # 3. Cursos
    cursos = conn.execute("SELECT * FROM cursos WHERE estado = 1 ORDER BY orden ASC").fetchall()
    
    # 4. Estadísticas (IMPORTANTE: Esto faltaba)
    # fetchall() trae una lista de todas las filas (Cursos, Profesores, Anuncios)
    estadisticas = conn.execute("SELECT * FROM estadisticas ORDER BY orden").fetchall()
    
    # 5. Nosotros (Para la sección de abajo)
    nosotros = conn.execute("SELECT * FROM nosotros LIMIT 1").fetchone()
    
    # 6. Valores (Las etiquetas de creatividad, pasión, etc.)
    valores = conn.execute("SELECT * FROM valores ORDER BY orden").fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                           configuracion=configuracion, 
                           hero=hero, 
                           cursos=cursos, 
                           estadisticas=estadisticas, # Ahora sí están definidas
                           nosotros=nosotros, 
                           valores=valores)
    
@app.route('/contacto', methods=['POST'])
def contacto():
    # Ahora 'request' ya funcionará porque está en el import de arriba
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')
    
    conn = get_db_connection()
    conn.execute("INSERT INTO mensajes_contacto (nombre, email, mensaje) VALUES (?, ?, ?)",
                 (nombre, email, mensaje))
    conn.commit()
    conn.close()
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)