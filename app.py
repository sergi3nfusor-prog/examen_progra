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
    
    
    # --- NUEVA LÓGICA PARA CARACTERÍSTICAS ---
    caracteristicas_db = conn.execute("SELECT * FROM curso_caracteristicas ORDER BY orden ASC").fetchall()    
    # Organizamos las características por el ID del curso
    caracteristicas_por_curso = {}
    for fila in caracteristicas_db:
        id_curso = fila['curso_id']
        if id_curso not in caracteristicas_por_curso:
            caracteristicas_por_curso[id_curso] = []
        caracteristicas_por_curso[id_curso].append(fila['caracteristica'])
    # ------------------------------------------
    
    
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
                           estadisticas=estadisticas,
                           nosotros=nosotros, 
                           valores=valores,
                           caracteristicas_por_curso=caracteristicas_por_curso) # Enviamos el diccionario
    

@app.route('/contacto', methods=['POST'])
def contacto():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')
    
    conn = get_db_connection()
    # Usamos 'mensajes_contacto' que es el nombre en tu DB
    conn.execute("INSERT INTO mensajes_contacto (nombre, email, mensaje) VALUES (?, ?, ?)",
                 (nombre, email, mensaje))
    conn.commit()
    conn.close()
    
    # Redirigir a la vista de la tabla
    return redirect(url_for('ver_mensajes'))

@app.route('/mensajes')
def ver_mensajes():
    conn = get_db_connection()
    # 'fecha_envio' es el nombre que aparece en tu captura de DBeaver
    mensajes = conn.execute("SELECT id, nombre, email, mensaje, fecha_envio FROM mensajes_contacto ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('mensajes.html', mensajes=mensajes)


@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM mensajes_contacto WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('ver_mensajes'))


if __name__ == '__main__':
    app.run(debug=True)