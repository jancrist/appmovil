from flask import Flask, render_template, request, redirect, url_for,flash, jsonify,send_file
import sqlite3
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename




app = Flask(__name__)
app.config['DATABASE'] = 'database.db'
app.secret_key = 'your_secret_key'
def get_db_connection():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with app.app_context():
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS casos (
                id INTEGER PRIMARY KEY,
                fecha_inicio TEXT,
                status TEXT,
                abogado_id INTEGER,
                cliente_id INTEGER,
                FOREIGN KEY (abogado_id) REFERENCES abogados (id),
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')

        # Crear la tabla "abogados"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS abogados (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                especialidad TEXT
            )
        ''')

        # Crear la tabla "clientes"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY,
                nombre TEXT,
                direccion TEXT,
                telefono TEXT
            )
        ''')

        # Crear la tabla "historial_casos"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historial_casos (
                id INTEGER PRIMARY KEY,
                caso_id INTEGER,
                nuevo_status TEXT,
                fecha_cambio TEXT,
                FOREIGN KEY (caso_id) REFERENCES casos (id)
            )
        ''')
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS documentacion (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        descripcion TEXT,
        archivo BLOB,
        caso_id INTEGER,
        FOREIGN KEY (caso_id) REFERENCES casos (id)
    )
''')



        db.commit()
        db.close()





















@app.route('/panel_estudio')
def panel_abogados():
   return render_template('panel_estudio.html')


@app.route('/estudio_casos')
def lista_casos():
    # Obtener la lista de casos de la base de datos (puedes utilizar SQLAlchemy para consultas más avanzadas)
    casos = []
    with app.app_context():
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM casos')
        casos = cursor.fetchall()

    return render_template('estudio_casos.html', casos=casos)

@app.route('/estudio_crear_caso')
def estudio_crear_caso():
    # Esta es la página para crear un nuevo caso
    return render_template('estudio_crear_caso.html')




def obtener_documentacion(caso_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Realiza una consulta para obtener la documentación relacionada con el caso_id
    cursor.execute('SELECT * FROM documentacion WHERE caso_id = ?', (caso_id,))
    documentacion = cursor.fetchall()

    conn.close()

    return documentacion


@app.route('/ver_documentacion/<int:caso_id>')
def ver_documentacion(caso_id):
    # Aquí obtén la documentación relacionada con el caso_id de la base de datos
    # Supongamos que documentacion es una lista de objetos Documento
    documentacion = obtener_documentacion(caso_id)  # Debes implementar esta función

    # Luego renderiza una plantilla HTML que muestre la documentación
    # Puedes pasar la documentación como contexto a la plantilla
    return render_template('ver_documentacion.html', caso_id=caso_id, documentacion=documentacion)






@app.route('/documentacion/')
def documentacion():
    # Renderiza la página de documentación
    return render_template('documentacion.html')













if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=1000)
