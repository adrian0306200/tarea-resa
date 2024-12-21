from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Configuración de la conexión a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bike_registry'

# Clave secreta para mensajes flash
app.secret_key = os.urandom(24)

mysql = MySQL(app)

@app.route('/')
def index():
    # Leer todas las bicicletas de la base de datos
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM bicycles')
    bicycles = cursor.fetchall()
    return render_template('index.html', bicycles=bicycles)

@app.route('/add', methods=['POST'])
def add_bicycle():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO bicycles (brand, model, year) VALUES (%s, %s, %s)', (brand, model, year))
        mysql.connection.commit()

        flash('Bicicleta agregada con éxito!')
        return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit_bicycle(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM bicycles WHERE id = %s', (id,))
    bicycle = cursor.fetchone()
    return render_template('edit.html', bicycle=bicycle)

@app.route('/update/<int:id>', methods=['POST'])
def update_bicycle(id):
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']

        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE bicycles
            SET brand = %s, model = %s, year = %s
            WHERE id = %s
        ''', (brand, model, year, id))
        mysql.connection.commit()

        flash('Bicicleta actualizada con éxito!')
        return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_bicycle(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM bicycles WHERE id = %s', (id,))
    mysql.connection.commit()

    flash('Bicicleta eliminada con éxito!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
