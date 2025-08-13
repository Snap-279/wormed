"""
Configuración de pytest para la aplicación Wormed
"""
import pytest
from app import create_app, db
from app.models.user import User, Role

@pytest.fixture
def app():
    """Crear instancia de la aplicación para testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        
        # Crear roles por defecto
        Role.get_or_create_default_roles()
        
        yield app
        
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Cliente de prueba Flask"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Runner de comandos CLI"""
    return app.test_cli_runner()

@pytest.fixture
def admin_user(app):
    """Usuario administrador para pruebas"""
    with app.app_context():
        admin_role = Role.query.filter_by(name='admin').first()
        user = User(
            email='admin@test.com',
            nombre='Admin',
            apellido='Test',
            role=admin_role,
            is_active=True
        )
        user.set_password('admin123')
        db.session.add(user)
        db.session.commit()
        return user

@pytest.fixture
def doctor_user(app):
    """Usuario doctor para pruebas"""
    with app.app_context():
        doctor_role = Role.query.filter_by(name='doctor').first()
        user = User(
            email='doctor@test.com',
            nombre='Doctor',
            apellido='Test',
            role=doctor_role,
            is_active=True
        )
        user.set_password('doctor123')
        db.session.add(user)
        db.session.commit()
        return user