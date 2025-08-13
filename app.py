#!/usr/bin/env python3
"""
Archivo principal de la aplicación Wormed
"""
import os
from app import create_app, db
from app.models.user import User, Role

# Crear instancia de la aplicación
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    """Provee contexto para shell de Flask"""
    return {
        'db': db,
        'User': User,
        'Role': Role
    }

@app.before_first_request
def create_tables():
    """Crear tablas y datos iniciales"""
    db.create_all()
    
    # Crear roles por defecto
    Role.get_or_create_default_roles()

if __name__ == '__main__':
    app.run(debug=True)