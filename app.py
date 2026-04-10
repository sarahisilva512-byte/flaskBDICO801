from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig
from models import db, Alumnos, Maestros, Cursos
import forms

# Importar Blueprints
from maestros.routes import maestros_bp
from cursos.routes import cursos_bp
from inscripciones.routes import inscripciones_bp

app = Flask(__name__)

# ==================== CONFIGURACIÓN DE BASE DE DATOS (SQLite) ====================
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'escuela.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# =============================================================================

app.config.from_object(DevelopmentConfig)

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

app.register_blueprint(maestros_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(inscripciones_bp)

# ========================== RUTAS ==========================

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

# ALUMNOS - Lista + Registro
@app.route("/Alumnos", methods=["GET", "POST"])
def alumnos():
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
        return redirect(url_for('alumnos'))
   
    lista_alumnos = Alumnos.query.all()
    return render_template("Alumnos.html", form=form, alumnos=lista_alumnos)


# MODIFICAR

@app.route("/modificar", methods=["GET", "POST"])
def modificar():
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
        flash("Alumno modificado correctamente")
        return redirect(url_for('alumnos'))
    
    return render_template("modificar.html", form=form)


# ELIMINAR

@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
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
        flash("Alumno eliminado correctamente")
        return redirect(url_for('alumnos'))
    
    return render_template("eliminar.html", form=form)



# DETALLES

@app.route("/detalles", methods=["GET"])
def detalles():
    id_alumno = request.args.get('id')
    if id_alumno:
        alum = Alumnos.query.get_or_404(id_alumno)
        return render_template("detalles.html",
                               id=alum.id,
                               nombre=alum.nombre,
                               apaterno=alum.apaterno,
                               amaterno=alum.amaterno,
                               edad=alum.edad,
                               email=alum.email)
    return redirect(url_for('alumnos'))


# ========================== EJECUCIÓN ==========================
if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
        print(f"Base de datos inicializada en: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.run(debug=True)