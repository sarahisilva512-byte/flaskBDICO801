from flask import render_template, request, redirect, url_for, flash
from . import cursos_bp
from models import db, Cursos, Maestros
import forms

# ====================== LISTA DE CURSOS ======================
@cursos_bp.route("/cursos", methods=["GET"])
def cursos():
    lista_cursos = Cursos.query.all()
    return render_template('cursos.html', cursos=lista_cursos)


# ====================== NUEVO CURSO ======================
@cursos_bp.route("/cursos/nuevo", methods=["GET", "POST"])
def nuevo_curso():
    form = forms.MaestroForm(request.form)  
    lista_maestros = Maestros.query.all()
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        maestro_id = request.form.get('maestro_id')
       
        if nombre and maestro_id:
            nuevo = Cursos(nombre=nombre, maestro_id=maestro_id)
            db.session.add(nuevo)
            db.session.commit()
            flash("Curso creado correctamente", "success")
            return redirect(url_for('cursos.cursos'))
    
    return render_template('nuevo_curso.html', form=form, maestros=lista_maestros)


# ====================== MODIFICAR CURSO (SOLO NOMBRE) ======================
@cursos_bp.route("/cursos/modificar", methods=["GET", "POST"])
def modificar_curso():
    if request.method == 'GET':
        id_curso = request.args.get('id')
        if id_curso:
            curso = Cursos.query.get_or_404(id_curso)
            form = forms.MaestroForm()
            return render_template('modificar_curso.html', curso=curso, form=form)
   
    if request.method == 'POST':
        id_curso = request.args.get('id')
        if not id_curso:
            id_curso = request.form.get('id')
        
        curso = Cursos.query.get_or_404(id_curso)
        nuevo_nombre = request.form.get('nombre')
        
        if nuevo_nombre:
            curso.nombre = nuevo_nombre
            db.session.commit()
            flash("Nombre del curso modificado correctamente", "success")
            return redirect(url_for('cursos.cursos'))
            form = forms.MaestroForm()
            return render_template('modificar_curso.html', curso=curso, form=form)


# ====================== ELIMINAR CURSO======================
@cursos_bp.route("/cursos/eliminar", methods=["GET", "POST"])
def eliminar_curso():
    if request.method == 'GET':
        id_curso = request.args.get('id')
        if id_curso:
            curso = Cursos.query.get_or_404(id_curso)
            return render_template('eliminar_curso.html', curso=curso)
    
    if request.method == 'POST':
        id_curso = request.form.get('id')
        if id_curso:
            curso = Cursos.query.get_or_404(id_curso)
            db.session.delete(curso)
            db.session.commit()
            flash("Curso eliminado correctamente", "success")
            return redirect(url_for('cursos.cursos'))
    
    return redirect(url_for('cursos.cursos'))


# ====================== DETALLES DEL CURSO ======================
@cursos_bp.route("/cursos/detalles", methods=["GET"])
def detalles_curso():
    id_curso = request.args.get('id')
    if id_curso:
        curso = Cursos.query.get_or_404(id_curso)
        return render_template('detalles_curso.html', curso=curso)
    return redirect(url_for('cursos.cursos'))