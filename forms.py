from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email, Optional, Length

# ====================== FORMULARIO PARA ALUMNOS ======================
class UserForm(FlaskForm):
    id = IntegerField("Matrícula / ID", [
        DataRequired(message="La matrícula es requerida")
    ])
    nombre = StringField('Nombre', [
        DataRequired(message="El nombre es requerido")
    ])
    apaterno = StringField('Apellido Paterno', [
        DataRequired(message="El apellido paterno es requerido")
    ])
    amaterno = StringField('Apellido Materno', [
        Optional()
    ])
    edad = IntegerField('Edad', [
        Optional()
    ])
    correo = EmailField('Correo Electrónico', [
        Email(message="Ingrese un correo válido"),
        Optional()
    ])


# ====================== FORMULARIO PARA MAESTROS ======================
class MaestroForm(FlaskForm):
    matricula = StringField('Matrícula', [
        DataRequired(message="La matrícula es requerida"),
        Length(min=3, max=15, message="La matrícula debe tener entre 3 y 15 caracteres")
    ])
    nombre = StringField('Nombre', [
        DataRequired(message="El nombre es requerido")
    ])
    apellidos = StringField('Apellidos', [
        DataRequired(message="Los apellidos son requeridos")
    ])
    especialidad = StringField('Especialidad', [
        DataRequired(message="La especialidad es requerida")
    ])
    correo = EmailField('Correo Electrónico', [
        Email(message="Ingrese un correo válido"),
        Optional()
    ])


# ====================== FORMULARIO PARA INSCRIPCIONES ======================
class InscripcionForm(FlaskForm):
    """Formulario simple usado principalmente para CSRF y validación básica"""
    alumno_id = HiddenField()
    curso_id = HiddenField()
    
   
# ====================== FORMULARIO PARA CURSOS ======================
class CursoForm(FlaskForm):
    nombre = StringField('Nombre del Curso', [
        DataRequired(message="El nombre del curso es requerido")
    ])
    descripcion = StringField('Descripción', [
        Optional()
    ])
    creditos = IntegerField('Créditos', [
        Optional()
    ])


# ====================== FORMULARIO PARA CONSULTAS======================
class ConsultasForm(FlaskForm):
    tipo_busqueda = SelectField(
        'Tipo de consulta',
        choices=[
            ('alumno', 'Alumno'),
            ('maestro', 'Maestro'),
            ('curso', 'Curso')
        ],
        validators=[DataRequired()]
    )

    termino = StringField(
        'Buscar',
        validators=[DataRequired(message="Ingresa un término")]
    )