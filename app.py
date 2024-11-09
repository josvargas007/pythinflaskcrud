from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conexión a la base de datos
conn = sqlite3.connect('almacen.db')
cursor = conn.cursor()

# Crear tabla productos si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY,
        descripcion TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio FLOAT NOT NULL
    )
''')

conn.commit()
conn.close()

# Rutas

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/productos')
def get_productos():
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/crear_producto', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        
        conn = sqlite3.connect('almacen.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO productos (descripcion, cantidad, precio) VALUES (?, ?, ?)', (descripcion, cantidad, precio))
        conn.commit()
        conn.close()
        
        return redirect(url_for('get_productos'))
    
    return render_template('crear_producto.html')

@app.route('/producto/<int:id>')
def get_producto(id):
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
    producto = cursor.fetchone()
    conn.close()
    
    if producto:
        return render_template('productos.html', producto=producto)
    else:
        return '<h1>Producto no encontrado</h1>'

@app.route('/actualizar_producto/<int:id>', methods=['GET', 'POST'])
def actualizar_producto(id):
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        
        conn = sqlite3.connect('almacen.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE productos SET descripcion = ?, cantidad = ?, precio = ? WHERE id = ?', (descripcion, cantidad, precio, id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('get_productos'))
    
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM productos WHERE id = ?', (id,))
    producto = cursor.fetchone()
    conn.close()
    
    if producto:
        return render_template('actualizar_producto.html', producto=producto)
    else:
        return '<h1>Producto no encontrado</h1>'

@app.route('/eliminar_producto/<int:id>')
def eliminar_producto(id):
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('get_productos'))

if __name__ == '__main__':
    app.run(debug=True)
