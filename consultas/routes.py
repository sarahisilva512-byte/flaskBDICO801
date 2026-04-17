from flask import render_template, flash
from . import consultas_bp
from models import Alumnos, Maestros, Cursos
from sqlalchemy import or_
from forms import ConsultasForm

@consultas_bp.route("/consultas", methods=["GET", "POST"])
def consultas():
    form = ConsultasForm()  

    resultados = None
    tipo_busqueda = None
    termino = None

    if form.validate_on_submit():
        tipo_busqueda = form.tipo_busqueda.data
        termino = form.termino.data.strip()

        if tipo_busqueda == "alumno":
            resultados = Alumnos.query.filter(
                or_(
                    Alumnos.nombre.ilike(f"%{termino}%"),
                    Alumnos.apaterno.ilike(f"%{termino}%"),
                    Alumnos.amaterno.ilike(f"%{termino}%")
                )
            ).all()

        elif tipo_busqueda == "maestro":
            resultados = Maestros.query.filter(
                or_(
                    Maestros.matricula.ilike(f"%{termino}%"),
                    Maestros.nombre.ilike(f"%{termino}%"),
                    Maestros.apellidos.ilike(f"%{termino}%")
                )
            ).all()

        elif tipo_busqueda == "curso":
            resultados = Cursos.query.filter(
                Cursos.nombre.ilike(f"%{termino}%")
            ).all()

        if not resultados:
            flash("No se encontraron resultados", "warning")

    return render_template(
        "consultas.html",
        form=form,   
        resultados=resultados,
        tipo_busqueda=tipo_busqueda,
        termino=termino
    )