from flask import render_template, request, redirect, session
from app_flask.modelos.modelo_paint import Paint
from app_flask import app

@app.route('/dashboard', methods=['GET'])
def desplegar_paint():
    if "id_usuario" not in session:
        return redirect('/')
    lista_paint = Paint.obtener_todos()
    return render_template('dashboard.html', lista_paint = lista_paint)

@app.route('/formulario/paint', methods=['GET'])
def desplegar_formulario_paint():
    if "id_usuario" not in session:
        return redirect('/')
    return render_template('formulario_paint.html')

@app.route('/crear/paint', methods=['POST'])
def crear_paint():
    if Paint.validar_paint(request.form) == False:
        return redirect('/formulario/paint')
    nuevo_paint = {
        **request.form,
        "id_usuario": session['id_usuario']
    }
    Paint.crear_uno(nuevo_paint)
    return redirect('/dashboard')

@app.route('/eliminar/paint/<int:id>', methods=['POST'])
def eliminar_paint(id):
    paint = {
        "id": id
    }
    Paint.elimina_uno(paint)
    return redirect('/dashboard')

@app.route('/formulario/editar/paint/<int:id>', methods=['GET'])
def despliega_formulario_editar_paint(id):
    if "id_usuario" not in session:
        return redirect('/')
    datos = {
        "id" : id
    }
    paint = Paint.obtener_uno(datos)
    return render_template('formulario_editar_paint.html', paint = paint)

@app.route('/editar/paint/<int:id>', methods=['POST'])
def editar_paint(id):
    if Paint.validar_paint(request.form) == False:
        return redirect(f'/formulario/editar/paint/{id}')
    editar_paint = {
        **request.form,
        "id" : id,
        "id_usuario" : session['id_usuario']
    }
    Paint.actualizar_uno(editar_paint)
    return redirect('/dashboard')

@app.route('/detalle/paint/<int:id>', methods=['GET'])
def desplegar_detalle_paint(id):
    if "id_usuario" not in session:
        return redirect('/')
    datos = {
        "id" : id
    }
    paint = Paint.obtener_uno_con_usuario(datos)
    return render_template('detalle_paint.html', paint = paint)