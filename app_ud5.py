# Se importan las librerias necesarias para desplegar la applicacion
from flask import Flask, render_template, request, redirect, url_for, flash

# Un script para administrar bases de datos
from dbmanager import sqlconnector

import os, sqlite3, uuid

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

# Creacion de base de datos
db = sqlconnector()

# La funcion espera como primer parametro el nombre de la tabla,
# y el resto de parametros los toma como atributos:
db.create_table('Empleados',
                'DNI INTEGER PRIMARY KEY', 
                'Nombre VARCHAR(45) NULL',
                'Apellidos VARCHAR(45) NULL',
                'Fecha_Nacimiento DATE NULL',
                'N_hijos INTEGER NULL',
                'estatura REAL NULL')

db.close()

@app.route('/')
def index():
    n_hijos = request.args.get('n_hijos', type=int)
    db = sqlconnector()
    empleados, column_names = db.obtener_empleados(n_hijos)
    db.close()
    return render_template(
            'empleados.html',
            empleados=empleados, 
            column_names=column_names
            )

@app.route('/agregar_empleado', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        dni = request.form['dni']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fn = request.form['fecha_nac']
        nh = request.form['n_hijos']
        estatura = request.form['estatura']
        
        error = False
        try:
            db = sqlconnector()
            db.insertar_empleado(dni, nombre, apellidos, fn, nh, estatura)
            flash('[*] Empleado registrado exitosamente.', 'success')
        except sqlite3.IntegrityError as e:
            error = True
            flash('[-] DNI ya existe', 'error')
        finally:
            db.close()
        
        if error:
            return redirect(url_for('add'))
        else:
            return redirect(url_for('index'))

    else:
        return render_template('form_empleado.html')

@app.route('/punto2_1')
def punto2_1():
    db = sqlconnector()
    empleados, column_names = db.punto2_1()
    db.close()
    return render_template('2_1.html', empleados=empleados, column_names=column_names)

@app.route('/punto2_2')
def punto2_2():
    db = sqlconnector()
    empleados, column_names = db.punto2_2()
    db.close()
    return render_template('2_2.html', empleados=empleados, column_names=column_names)

@app.route('/punto2_3')
def punto2_3():
    db = sqlconnector()
    empleados, column_names = db.obtener_nulls()
    db.close()
    return render_template('2_3.html', empleados=empleados, column_names=column_names)

@app.route('/punto2_4')
def punto2_4():
    error = False
    try:
        db = sqlconnector()
        db.nueva_columna()
    except sqlite3.OperationalError as e:
        error = True
    finally:
        db.close()
    if error:
        flash('[-] La columna ya ha sido creada', 'error')
        return redirect(url_for('index'))
    else:
        flash('[*] Nueva columna creada exitosamente', 'success')
        return redirect(url_for('index'))
