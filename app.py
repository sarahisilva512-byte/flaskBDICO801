from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig
from models import db

# ==================== IMPORTAR BLUEPRINTS ====================
from alumnos.routes import alumnos_bp
from maestros.routes import maestros_bp
from cursos.routes import cursos_bp
from inscripciones.routes import inscripciones_bp
from consultas.routes import consultas_bp
# ===========================================================

app = Flask(__name__)

# ==================== CONFIGURACIÓN DE BASE DE DATOS ====================
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'escuela.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# =====================================================================

app.config.from_object(DevelopmentConfig)

# Inicializar extensiones
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

# Registrar todos los blueprints
app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)
app.register_blueprint(cursos_bp)
app.register_blueprint(inscripciones_bp)
app.register_blueprint(consultas_bp)

# ========================== RUTAS PRINCIPALES ==========================

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

# ========================== EJECUCIÓN ==========================
if __name__ == '__main__':
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
        print(f"Base de datos inicializada en: {app.config['SQLALCHEMY_DATABASE_URI']}")
    app.run(debug=True)