from flask import render_template
from . import consultas_bp
from models import Cursos

# Consultas: Ver alumnos inscritos por curso
@consultas_bp.route("/consultas/curso/<int:curso_id>")
def alumnos_por_curso(curso_id):
    curso = Cursos.query.get_or_404(curso_id)
    return render_template("consultas/alumnos_por_curso.html", curso=curso)

# Consultas: Ver cursos en los que está inscrito un alumno
@consultas_bp.route("/consultas/alumno/<int:alumno_id>")
def cursos_por_alumno(alumno_id):
    # Esta ruta la puedes implementar después si la necesitas
    pass