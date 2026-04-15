# cursos/routes.py
from flask import render_template, request, redirect, url_for, flash
from . import cursos_bp
from models import db, Cursos, Maestros
import forms

# Lista + Crear Curso
@cursos_bp.route("/cursos", methods=["GET", "POST"])
def cursos():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        maestro_id = request.form.get('maestro_id')
        
        if nombre and maestro_id:
            nuevo = Cursos(nombre=nombre, maestro_id=maestro_id)
            db.session.add(nuevo)
            db.session.commit()
            flash("Curso creado correctamente")
            return redirect(url_for('cursos.cursos'))
    
    lista_cursos = Cursos.query.all()
    lista_maestros = Maestros.query.all()
    return render_template('cursos.html', cursos=lista_cursos, maestros=lista_maestros)


# Nuevo Curso (Página separada)
@cursos_bp.route("/cursos/nuevo", methods=["GET"])
def nuevo_curso():
    form = forms.MaestroForm(request.form)   # Solo para CSRF
    lista_maestros = Maestros.query.all()
    return render_template('nuevo_curso.html', form=form, maestros=lista_maestros)


# Modificar Curso
@cursos_bp.route("/cursos/modificar", methods=["GET", "POST"])
def modificar_curso():
    if request.method == 'GET':
        id_curso = request.args.get('id')
        if id_curso:
            curso = Cursos.query.get_or_404(id_curso)
            return render_template('modificar_curso.html', curso=curso)
    
    # POST - Guardar cambios
    id_curso = request.args.get('id')
    curso = Cursos.query.get_or_404(id_curso)
    curso.nombre = request.form.get('nombre')
    curso.maestro_id = request.form.get('maestro_id')
    
    db.session.commit()
    flash("Curso modificado correctamente")
    return redirect(url_for('cursos.cursos'))


# Eliminar Curso
@cursos_bp.route("/cursos/eliminar", methods=["GET", "POST"])
def eliminar_curso():
    id_curso = request.args.get('id')
    if id_curso:
        curso = Cursos.query.get_or_404(id_curso)
        db.session.delete(curso)
        db.session.commit()
        flash("Curso eliminado correctamente")
    return redirect(url_for('cursos.cursos'))


# Detalles del Curso
@cursos_bp.route("/cursos/detalles", methods=["GET"])
def detalles_curso():
    id_curso = request.args.get('id')
    if id_curso:
        curso = Cursos.query.get_or_404(id_curso)
        return render_template('detalles_curso.html', curso=curso)
    return redirect(url_for('cursos.cursos'))