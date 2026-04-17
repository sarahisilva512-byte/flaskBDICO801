from flask import render_template, request, redirect, url_for, flash
from . import inscripciones_bp
from models import db, Alumnos, Cursos
import forms

# ====================== LISTA DE INSCRIPCIONES ======================
@inscripciones_bp.route("/inscripciones", methods=["GET"])
def inscripciones():
    cursos = Cursos.query.all()
    return render_template('inscripciones.html', cursos=cursos)


# ====================== NUEVA INSCRIPCIÓN ======================
@inscripciones_bp.route("/inscripciones/nueva", methods=["GET", "POST"])
def nueva_inscripcion():
    if request.method == 'POST':
        alumno_id = request.form.get('alumno_id')
        curso_id = request.form.get('curso_id')
       
        if alumno_id and curso_id:
            alumno = Alumnos.query.get_or_404(alumno_id)
            curso = Cursos.query.get_or_404(curso_id)
           
            if curso in alumno.cursos:
                flash("Este alumno ya está inscrito en este curso", "danger")
            else:
                alumno.cursos.append(curso)
                db.session.commit()
                flash(f"{alumno.nombre} ha sido inscrito correctamente en {curso.nombre}", "success")
                return redirect(url_for('inscripciones.nueva_inscripcion', curso_id=curso_id))
                curso_id = request.args.get('curso_id')
                curso = None
                if curso_id:
                    curso = Cursos.query.get_or_404(curso_id)
                
                alumnos = Alumnos.query.all()
                form = forms.MaestroForm()   
                return render_template('nueva_inscripcion.html', 
                                    form=form, 
                                    alumnos=alumnos, 
                                    curso=curso)


@inscripciones_bp.route("/inscripciones/eliminar", methods=["POST"])
def eliminar_inscripcion():
    alumno_id = request.form.get('alumno_id')
    curso_id = request.form.get('curso_id')
   
    if alumno_id and curso_id:
        alumno = Alumnos.query.get_or_404(alumno_id)
        curso = Cursos.query.get_or_404(curso_id)
       
        if curso in alumno.cursos:
            alumno.cursos.remove(curso)
            db.session.commit()
            flash("Inscripción eliminada correctamente", "success")
   
    return redirect(url_for('inscripciones.inscripciones'))