# maestros/routes.py


from flask import render_template, request, redirect, url_for, flash
from . import maestros_bp
import forms
from models import db, Maestros


# LISTA + REGISTRO 
@maestros_bp.route("/maestros", methods=["GET", "POST"])
def maestros():
    form = forms.MaestroForm(request.form)
   
    if request.method == 'POST' and form.validate():
        nuevo = Maestros(
            matricula=form.matricula.data,
            nombre=form.nombre.data,
            apellidos=form.apellidos.data,
            especialidad=form.especialidad.data,
            email=form.correo.data
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("Maestro guardado correctamente")
        return redirect(url_for('maestros.maestros'))
   
    lista = Maestros.query.all()
    return render_template('maestros.html', form=form, maestros=lista)


# NUEVO MAESTRO 
@maestros_bp.route("/maestros/nuevo", methods=["GET"])
def nuevo_maestro():
    form = forms.MaestroForm(request.form)
    return render_template('nuevo_maestro.html', form=form)


#  MODIFICAR MAESTRO 
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
        maestro = Maestros.query.get_or_404(id_maestro)
        
        maestro.matricula = form.matricula.data
        maestro.nombre = form.nombre.data
        maestro.apellidos = form.apellidos.data
        maestro.especialidad = form.especialidad.data
        maestro.email = form.correo.data
        
        db.session.commit()
        flash("Maestro modificado correctamente")
        return redirect(url_for('maestros.maestros'))
    
    return render_template('modificar_maestro.html', form=form)


# ELIMINAR MAESTRO (Corregido y mejorado como en Cursos)
@maestros_bp.route("/maestros/eliminar", methods=["GET", "POST"])
def eliminar_maestro():
    if request.method == 'POST':
        id_maestro = request.form.get('id')          # ← Recibe el id desde el formulario
        if id_maestro:
            maestro = Maestros.query.get_or_404(id_maestro)
            db.session.delete(maestro)
            db.session.commit()
            flash("Maestro eliminado correctamente")
        else:
            flash("Error: No se recibió el ID del maestro", "danger")
    
    # Siempre redirigir después de eliminar
    return redirect(url_for('maestros.maestros'))


#  DETALLES MAESTRO 
@maestros_bp.route("/maestros/detalles", methods=["GET"])
def detalles_maestro():
    id_maestro = request.args.get('id')
    if id_maestro:
        maestro = Maestros.query.get_or_404(id_maestro)
        return render_template('detalles_maestro.html', maestro=maestro)
    return redirect(url_for('maestros.maestros'))
