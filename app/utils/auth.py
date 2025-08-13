"""
Utilidades de autenticación y seguridad
"""
import bcrypt
from functools import wraps
from flask import redirect, url_for, flash, request
from flask_login import current_user

def hash_password(password):
    """
    Hashea una contraseña usando bcrypt
    
    Args:
        password (str): Contraseña en texto plano
        
    Returns:
        str: Contraseña hasheada
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def check_password(password, password_hash):
    """
    Verifica una contraseña contra su hash
    
    Args:
        password (str): Contraseña en texto plano
        password_hash (str): Hash almacenado
        
    Returns:
        bool: True si la contraseña es correcta
    """
    password_bytes = password.encode('utf-8')
    password_hash_bytes = password_hash.encode('utf-8')
    return bcrypt.checkpw(password_bytes, password_hash_bytes)

def admin_required(f):
    """
    Decorador que requiere rol de administrador
    
    Args:
        f: Función a decorar
        
    Returns:
        function: Función decorada
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        if not current_user.is_admin():
            flash('No tienes permisos para acceder a esta página.', 'error')
            return redirect(url_for('main.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function

def doctor_required(f):
    """
    Decorador que requiere rol de doctor o admin
    
    Args:
        f: Función a decorar
        
    Returns:
        function: Función decorada
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        if not (current_user.is_doctor() or current_user.is_admin()):
            flash('No tienes permisos para acceder a esta página.', 'error')
            return redirect(url_for('main.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function