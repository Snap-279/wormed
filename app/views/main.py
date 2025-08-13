"""
Blueprint principal de la aplicación
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.utils.auth import admin_required, doctor_required
from app.models.user import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página de inicio"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal"""
    return render_template('main/dashboard.html')

@main_bp.route('/usuarios')
@admin_required
def usuarios():
    """Lista de usuarios (solo admin)"""
    users = User.query.all()
    return render_template('main/usuarios.html', users=users)

@main_bp.route('/perfil')
@login_required
def perfil():
    """Perfil del usuario actual"""
    return render_template('main/perfil.html')