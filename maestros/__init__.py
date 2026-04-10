# maestros/__init__.py
from flask import Blueprint

maestros_bp = Blueprint('maestros', __name__, 
                        template_folder='templates')