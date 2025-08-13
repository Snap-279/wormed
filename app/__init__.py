"""
Factory de la aplicación Flask Wormed
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from config import config

# Instancias de extensiones
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app(config_name='default'):
    """
    Factory de la aplicación Flask
    
    Args:
        config_name (str): Nombre de la configuración a usar
        
    Returns:
        Flask: Instancia de la aplicación configurada
    """
    app = Flask(__name__)
    
    # Configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Configuración de Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Registrar Blueprints
    from app.views.auth import auth_bp
    from app.views.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    # Comando CLI para crear usuario admin
    @app.cli.command()
    def create_admin():
        """Crear usuario administrador por defecto"""
        from app.models.user import User, Role
        from app.utils.auth import hash_password
        
        # Crear rol admin si no existe
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrador del sistema')
            db.session.add(admin_role)
        
        # Crear usuario admin si no existe
        admin_user = User.query.filter_by(email=app.config['ADMIN_EMAIL']).first()
        if not admin_user:
            admin_user = User(
                email=app.config['ADMIN_EMAIL'],
                nombre='Administrador',
                apellido='Sistema',
                password_hash=hash_password(app.config['ADMIN_PASSWORD']),
                role=admin_role,
                is_active=True
            )
            db.session.add(admin_user)
            db.session.commit()
            print(f'Usuario admin creado: {app.config["ADMIN_EMAIL"]}')
        else:
            print('Usuario admin ya existe')
    
    return app