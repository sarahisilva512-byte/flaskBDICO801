from flask import render_template, request, redirect, url_for, flash
from . import alumnos_bp
import forms
from models import db, Alumnos

# ====================== LISTA + CREAR ALUMNO ======================
@alumnos_bp.route("/Alumnos", methods=["GET", "POST"])
def alumnos():
    form = forms.UserForm(request.form)
  
    if request.method == 'POST' and form.validate():
        # Validar que la matrícula (id) no exista
        if Alumnos.query.filter_by(id=form.id.data).first():
            flash("Esta matrícula ya existe. Por favor usa otra.", "danger")
        else:
            nuevo = Alumnos(
                id=form.id.data,
                nombre=form.nombre.data,
                apaterno=form.apaterno.data,
                amaterno=form.amaterno.data,
                edad=form.edad.data,
                email=form.correo.data
            )
            db.session.add(nuevo)
            db.session.commit()
            flash("Alumno guardado correctamente", "success")
            return redirect(url_for('alumnos.alumnos'))
  
    lista_alumnos = Alumnos.query.all()
    return render_template("Alumnos.html", form=form, alumnos=lista_alumnos)


# ====================== NUEVO ALUMNO (Página separada) ======================
@alumnos_bp.route("/alumnos/nuevo", methods=["GET", "POST"])
def nuevo_alumno():
    form = forms.UserForm(request.form)
  
    if request.method == 'POST' and form.validate():
        if Alumnos.query.filter_by(id=form.id.data).first():
            flash("Esta matrícula ya existe. Por favor usa otra.", "danger")
        else:
            nuevo = Alumnos(
                id=form.id.data,
                nombre=form.nombre.data,
                apaterno=form.apaterno.data,
                amaterno=form.amaterno.data,
                edad=form.edad.data,
                email=form.correo.data
            )
            db.session.add(nuevo)
            db.session.commit()
            flash("Alumno guardado correctamente", "success")
            # NO redirigimos, nos quedamos en la misma página
            # return redirect(...)  ← Comentado a propósito

    return render_template("nuevo_alumno.html", form=form)


# ====================== MODIFICAR ALUMNO ======================
@alumnos_bp.route("/alumnos/modificar_alumno", methods=["GET", "POST"])
def modificar_alumno():
    form = forms.UserForm(request.form)
  
    if request.method == 'GET':
        id_alumno = request.args.get('id')
        if id_alumno:
            alum = Alumnos.query.get_or_404(id_alumno)
            form.id.data = alum.id
            form.nombre.data = alum.nombre
            form.apaterno.data = alum.apaterno
            form.amaterno.data = alum.amaterno
            form.edad.data = alum.edad
            form.correo.data = alum.email
  
    if request.method == 'POST' and form.validate():
        id_alumno = form.id.data
        alum = Alumnos.query.get_or_404(id_alumno)
      
        alum.nombre = form.nombre.data
        alum.apaterno = form.apaterno.data
        alum.amaterno = form.amaterno.data
        alum.edad = form.edad.data
        alum.email = form.correo.data
      
        db.session.commit()
        flash("Alumno modificado correctamente", "success")
        return redirect(url_for('alumnos.alumnos'))
  
    return render_template("modificar_alumno.html", form=form)


# ====================== ELIMINAR ALUMNO ======================
@alumnos_bp.route("/alumnos/eliminar_alumno", methods=["GET", "POST"])
def eliminar_alumno():
    form = forms.UserForm(request.form)
  
    if request.method == 'GET':
        id_alumno = request.args.get('id')
        if id_alumno:
            alum = Alumnos.query.get_or_404(id_alumno)
            form.id.data = alum.id
            form.nombre.data = alum.nombre
            form.apaterno.data = alum.apaterno
            form.amaterno.data = alum.amaterno
            form.edad.data = alum.edad
            form.correo.data = alum.email
 
    if request.method == 'POST':
        id_alumno = form.id.data
        alum = Alumnos.query.get_or_404(id_alumno)
        db.session.delete(alum)
        db.session.commit()
        flash("Alumno eliminado correctamente", "success")
        return redirect(url_for('alumnos.alumnos'))
  
    return render_template("eliminar_alumno.html", form=form)


# ====================== DETALLES ALUMNO ======================
@alumnos_bp.route("/alumnos/detalles_alumno", methods=["GET"])
def detalles_alumno():
    id_alumno = request.args.get('id')
    if id_alumno:
        alum = Alumnos.query.get_or_404(id_alumno)
        return render_template("detalles_alumno.html",
                               id=alum.id,
                               nombre=alum.nombre,
                               apaterno=alum.apaterno,
                               amaterno=alum.amaterno,
                               edad=alum.edad,
                               email=alum.email)
    return redirect(url_for('alumnos.alumnos'))