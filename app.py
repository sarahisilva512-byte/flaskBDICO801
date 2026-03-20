from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig

from models import db, Alumnos, Maestros, Cursos
import forms

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

@app.route("/")
def index():
    return render_template("index.html")



# ALUMNOS

@app.route("/usuarios", methods=["GET", "POST"])
def usuario():
    form = forms.UserForm(request.form)

    if request.method == 'POST' and form.validate():
        nuevo = Alumnos(
            nombre=form.nombre.data,
            apaterno=form.apaterno.data,
            amaterno=form.amaterno.data,
            edad=form.edad.data,
            email=form.correo.data
        )
        db.session.add(nuevo)
        db.session.commit()

        flash("Alumno guardado correctamente")
        return redirect(url_for('usuario'))

    lista = Alumnos.query.all()
    return render_template('usuarios.html', form=form, alumnos=lista)


# MAESTROS

@app.route("/maestros", methods=["GET", "POST"])
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
        return redirect(url_for('maestros'))

    lista = Maestros.query.all()
    return render_template('maestros.html', form=form, maestros=lista)


# CURSOS

@app.route("/cursos", methods=["GET", "POST"])
def cursos():

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        maestro_id = request.form.get('maestro_id')

        if nombre and maestro_id:
            nuevo = Cursos(nombre=nombre, maestro_id=maestro_id)
            db.session.add(nuevo)
            db.session.commit()

            flash("Curso creado correctamente")

        return redirect(url_for('cursos'))

    lista = Cursos.query.all()
    maestros = Maestros.query.all()

    return render_template('cursos.html', cursos=lista, maestros=maestros)



# CONSULTAS

@app.route("/consultas/alumno/<int:id>/cursos")
def cursos_de_alumno(id):
    alumno = Alumnos.query.get_or_404(id)
    return render_template("cursos_alumno.html", alumno=alumno)


@app.route("/consultas/curso/<int:id>/alumnos")
def alumnos_de_curso(id):
    curso = Cursos.query.get_or_404(id)
    return render_template("alumnos_curso.html", curso=curso)


if __name__ == '__main__':
    csrf.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(debug=True)