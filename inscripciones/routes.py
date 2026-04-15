# inscripciones/routes.py


from flask import render_template, request, redirect, url_for, flash
from . import inscripciones_bp
from models import db, Alumnos, Cursos
import forms

# Lista de Inscripciones
@inscripciones_bp.route("/inscripciones", methods=["GET"])
def inscripciones():
    cursos = Cursos.query.all()
    return render_template('inscripciones.html', cursos=cursos)


# Nueva Inscripción
@inscripciones_bp.route("/inscripciones/nueva", methods=["GET", "POST"])
def nueva_inscripcion():
    if request.method == 'POST':
        alumno_id = request.form.get('alumno_id')
        curso_id = request.form.get('curso_id')
        
        if alumno_id and curso_id:
            alumno = Alumnos.query.get(alumno_id)
            curso = Cursos.query.get(curso_id)
            
            if alumno and curso:
                if curso not in alumno.cursos:
                    alumno.cursos.append(curso)
                    db.session.commit()
                    flash(f"{alumno.nombre} ha sido inscrito en {curso.nombre} correctamente")
                else:
                    flash("El alumno ya está inscrito en este curso")
                
                return redirect(url_for('inscripciones.inscripciones'))
    
    form = forms.MaestroForm(request.form)
    alumnos = Alumnos.query.all()
    cursos = Cursos.query.all()
    return render_template('nueva_inscripcion.html', form=form, alumnos=alumnos, cursos=cursos)


# Ver Alumnos inscritos en un curso
@inscripciones_bp.route("/inscripciones/curso/<int:curso_id>/alumnos", methods=["GET"])
def ver_alumnos_curso(curso_id):
    curso = Cursos.query.get_or_404(curso_id)
    return render_template('ver_alumnos_curso.html', curso=curso)


# Eliminar Inscripción Individual
@inscripciones_bp.route("/inscripciones/eliminar", methods=["POST"])
def eliminar_inscripcion():
    alumno_id = request.form.get('alumno_id')
    curso_id = request.form.get('curso_id')
    
    if alumno_id and curso_id:
        alumno = Alumnos.query.get(alumno_id)
        curso = Cursos.query.get(curso_id)
        
        if alumno and curso and curso in alumno.cursos:
            alumno.cursos.remove(curso)
            db.session.commit()
            flash("Inscripción eliminada correctamente")
    
    return redirect(url_for('inscripciones.inscripciones'))