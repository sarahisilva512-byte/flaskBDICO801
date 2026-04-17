from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ====================== TABLA INTERMEDIA  ======================
alumno_curso = db.Table('alumno_curso',
    db.Column('alumno_id', db.Integer, db.ForeignKey('alumnos.id'), primary_key=True),
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id'), primary_key=True)
)

# ====================== MODELO ALUMNOS ======================
class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apaterno = db.Column(db.String(50), nullable=False)
    amaterno = db.Column(db.String(150), nullable=True)
    edad = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    # Relación Many-to-Many
    cursos = db.relationship('Cursos', secondary=alumno_curso, backref=db.backref('alumnos', lazy='dynamic'))

    def __repr__(self):
        return f'<Alumnos {self.nombre} {self.apaterno}>'

# ====================== MODELO MAESTROS ======================
class Maestros(db.Model):
    __tablename__ = 'maestros'
    
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.String(20), unique=True, nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True)

    cursos = db.relationship('Cursos', backref='maestro', lazy=True)

    def __repr__(self):
        return f'<Maestros {self.nombre} {self.apellidos}>'

# ====================== MODELO CURSOS ======================
class Cursos(db.Model):
    __tablename__ = 'cursos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    maestro_id = db.Column(db.Integer, db.ForeignKey('maestros.id'), nullable=False)

    def __repr__(self):
        return f'<Cursos {self.nombre}>'

# ====================== MODELO INSCRIPCIONES ======================
class Inscripciones(db.Model):
    __tablename__ = 'inscripciones'
    
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    alumno = db.relationship('Alumnos', backref='inscripciones')
    curso = db.relationship('Cursos', backref='inscripciones')

    def __repr__(self):
        return f'<Inscripcion Alumno:{self.alumno_id} - Curso:{self.curso_id}>'

# ====================== MODELO CONSULTAS ======================
class Consultas(db.Model):
    __tablename__ = 'consultas'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo_consulta = db.Column(db.String(50), nullable=False)  
    descripcion = db.Column(db.Text, nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Consulta {self.tipo_consulta}>'