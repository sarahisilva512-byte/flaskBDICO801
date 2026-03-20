from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

alumno_curso = db.Table('alumno_curso',
    db.Column('alumno_id', db.Integer, db.ForeignKey('alumnos.id')),
    db.Column('curso_id', db.Integer, db.ForeignKey('cursos.id'))
)

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apaterno = db.Column(db.String(50), nullable=False)
    amaterno = db.Column(db.String(150), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), nullable=False)


class Maestros(db.Model):
    __tablename__ = 'maestros'
    id = db.Column(db.Integer, primary_key=True)
    matricula = db.Column(db.Integer)
    nombre = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    especialidad = db.Column(db.String(50))
    email = db.Column(db.String(50))

    cursos = db.relationship('Cursos', backref='maestro')


class Cursos(db.Model):
    __tablename__ = 'cursos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))

    maestro_id = db.Column(db.Integer, db.ForeignKey('maestros.id'))

    alumnos = db.relationship('Alumnos', secondary=alumno_curso, backref='cursos')