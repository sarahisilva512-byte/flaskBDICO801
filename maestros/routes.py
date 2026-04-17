from flask import render_template, request, redirect, url_for, flash
from . import maestros_bp
import forms
from models import db, Maestros

# ====================== LISTA DE MAESTROS ======================
@maestros_bp.route("/maestros", methods=["GET"])
def maestros():
    lista = Maestros.query.all()
    return render_template('maestros.html', maestros=lista)


# ====================== NUEVO MAESTRO ======================
@maestros_bp.route("/maestros/nuevo", methods=["GET", "POST"])
def nuevo_maestro():
    form = forms.MaestroForm(request.form)
   
    if request.method == 'POST' and form.validate():
        if Maestros.query.filter_by(matricula=form.matricula.data).first():
            flash("Esta matrícula ya existe. Por favor usa otra.", "danger")
        else:
            nuevo = Maestros(
                matricula=form.matricula.data,
                nombre=form.nombre.data,
                apellidos=form.apellidos.data,
                especialidad=form.especialidad.data,
                email=form.correo.data
            )
            db.session.add(nuevo)
            db.session.commit()
            flash("¡Maestro registrado correctamente!", "success")
            return redirect(url_for('maestros.maestros'))
            return render_template('nuevo_maestro.html', form=form)


# ====================== MODIFICAR MAESTRO ======================
@maestros_bp.route("/maestros/modificar", methods=["GET", "POST"])
def modificar_maestro():
    form = forms.MaestroForm(request.form)
   
    if request.method == 'GET':
        id_maestro = request.args.get('id')
        if id_maestro:
            maestro = Maestros.query.get_or_404(id_maestro)
            form.matricula.data = maestro.matricula
            form.nombre.data = maestro.nombre
            form.apellidos.data = maestro.apellidos
            form.especialidad.data = maestro.especialidad
            form.correo.data = maestro.email

    if request.method == 'POST' and form.validate():
        id_maestro = request.args.get('id')
        if not id_maestro:
            id_maestro = request.form.get('id')
        maestro = Maestros.query.get_or_404(id_maestro)
       
        nueva_matricula = form.matricula.data
        existing = Maestros.query.filter_by(matricula=nueva_matricula).first()
       
        if existing and existing.id != maestro.id:
            flash("Esta matrícula ya existe. Por favor usa otra.", "danger")
        else:
            maestro.nombre = form.nombre.data
            maestro.apellidos = form.apellidos.data
            maestro.especialidad = form.especialidad.data
            maestro.email = form.correo.data
           
            db.session.commit()
            flash("¡Maestro modificado correctamente!", "success")
            return redirect(url_for('maestros.maestros'))
    
    return render_template('modificar_maestro.html', form=form)


# ====================== ELIMINAR MAESTRO ======================
@maestros_bp.route("/maestros/eliminar", methods=["GET", "POST"])
def eliminar_maestro():
    form = forms.MaestroForm(request.form)
   
    if request.method == 'GET':
        id_maestro = request.args.get('id')
        if id_maestro:
            maestro = Maestros.query.get_or_404(id_maestro)
            form.matricula.data = maestro.matricula
            form.nombre.data = maestro.nombre
            form.apellidos.data = maestro.apellidos
            form.especialidad.data = maestro.especialidad
            form.correo.data = maestro.email

    if request.method == 'POST':
        id_maestro = request.form.get('id')
        if id_maestro:
            maestro = Maestros.query.get_or_404(id_maestro)
            for curso in maestro.cursos:
                for alumno in curso.alumnos.all():
                    curso.alumnos.remove(alumno)

                db.session.delete(curso)
                db.session.delete(maestro)
                db.session.commit()

            flash("Maestro y sus cursos eliminados correctamente", "success")
            return redirect(url_for('maestros.maestros'))
    
    return render_template('eliminar_maestro.html', form=form)


# ====================== DETALLES MAESTRO ======================
@maestros_bp.route("/maestros/detalles", methods=["GET"])
def detalles_maestro():
    id_maestro = request.args.get('id')
    if id_maestro:
        maestro = Maestros.query.get_or_404(id_maestro)
        return render_template('detalles_maestro.html', maestro=maestro)
    return redirect(url_for('maestros.maestros'))