"""
Tests para los modelos de la aplicación
"""
import pytest
from app import db
from app.models.user import User, Role

class TestRole:
    """Tests para el modelo Role"""
    
    def test_role_creation(self, app):
        """Probar creación de rol"""
        with app.app_context():
            role = Role(name='test_role', description='Rol de prueba')
            db.session.add(role)
            db.session.commit()
            
            assert role.id is not None
            assert role.name == 'test_role'
            assert role.description == 'Rol de prueba'
            assert role.created_at is not None
    
    def test_role_repr(self, app):
        """Probar representación string del rol"""
        with app.app_context():
            role = Role(name='test_role')
            assert str(role) == '<Role test_role>'
    
    def test_get_or_create_default_roles(self, app):
        """Probar creación de roles por defecto"""
        with app.app_context():
            roles = Role.get_or_create_default_roles()
            
            assert len(roles) >= 2
            admin_role = Role.query.filter_by(name='admin').first()
            doctor_role = Role.query.filter_by(name='doctor').first()
            
            assert admin_role is not None
            assert doctor_role is not None
            assert admin_role.description == 'Administrador del sistema con acceso completo'
            assert doctor_role.description == 'Doctor con acceso a notas clínicas'

class TestUser:
    """Tests para el modelo User"""
    
    def test_user_creation(self, app, admin_user):
        """Probar creación de usuario"""
        with app.app_context():
            user = User.query.filter_by(email='admin@test.com').first()
            
            assert user is not None
            assert user.email == 'admin@test.com'
            assert user.nombre == 'Admin'
            assert user.apellido == 'Test'
            assert user.is_active is True
            assert user.created_at is not None
            assert user.role.name == 'admin'
    
    def test_user_repr(self, app, admin_user):
        """Probar representación string del usuario"""
        with app.app_context():
            user = User.query.filter_by(email='admin@test.com').first()
            assert str(user) == '<User admin@test.com>'
    
    def test_nombre_completo(self, app, admin_user):
        """Probar propiedad nombre_completo"""
        with app.app_context():
            user = User.query.filter_by(email='admin@test.com').first()
            assert user.nombre_completo == 'Admin Test'
    
    def test_password_hashing(self, app, admin_user):
        """Probar hashing y verificación de contraseñas"""
        with app.app_context():
            user = User.query.filter_by(email='admin@test.com').first()
            
            # Verificar que la contraseña correcta funciona
            assert user.check_password('admin123') is True
            # Verificar que una contraseña incorrecta no funciona
            assert user.check_password('wrongpassword') is False
    
    def test_set_password(self, app, admin_user):
        """Probar establecer nueva contraseña"""
        with app.app_context():
            user = User.query.filter_by(email='admin@test.com').first()
            
            user.set_password('newpassword123')
            db.session.commit()
            
            assert user.check_password('newpassword123') is True
            assert user.check_password('admin123') is False
    
    def test_role_methods(self, app, admin_user, doctor_user):
        """Probar métodos de verificación de roles"""
        with app.app_context():
            admin = User.query.filter_by(email='admin@test.com').first()
            doctor = User.query.filter_by(email='doctor@test.com').first()
            
            # Test admin user
            assert admin.has_role('admin') is True
            assert admin.has_role('doctor') is False
            assert admin.is_admin() is True
            assert admin.is_doctor() is False
            
            # Test doctor user
            assert doctor.has_role('doctor') is True
            assert doctor.has_role('admin') is False
            assert doctor.is_admin() is False
            assert doctor.is_doctor() is True
    
    def test_update_last_login(self, app, admin_user):
        """Probar actualización de último login"""
        with app.app_context():
            user = User.query.filter_by(email='admin@test.com').first()
            original_last_login = user.last_login
            
            user.update_last_login()
            
            assert user.last_login is not None
            assert user.last_login != original_last_login