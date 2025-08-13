"""
Tests para autenticación y vistas
"""
import pytest
from flask import url_for
from app import db
from app.models.user import User, Role

class TestAuthViews:
    """Tests para las vistas de autenticación"""
    
    def test_login_page(self, client):
        """Probar que la página de login se carga correctamente"""
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Wormed' in response.data
        assert 'Sistema de Gestión Clínica'.encode('utf-8') in response.data
    
    def test_registro_page(self, client):
        """Probar que la página de registro se carga correctamente"""
        response = client.get('/auth/registro')
        assert response.status_code == 200
        assert b'Crear Cuenta' in response.data
        assert 'Regístrate en Wormed'.encode('utf-8') in response.data
    
    def test_login_redirect_when_authenticated(self, client, admin_user):
        """Probar redirección cuando usuario ya está autenticado"""
        with client.session_transaction() as sess:
            sess['_user_id'] = str(admin_user.id)
            sess['_fresh'] = True
        
        response = client.get('/auth/login')
        assert response.status_code == 302
    
    def test_successful_login(self, client, admin_user):
        """Probar login exitoso"""
        response = client.post('/auth/login', data={
            'email': 'admin@test.com',
            'password': 'admin123',
            'csrf_token': 'test'  # En testing, CSRF está deshabilitado
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert b'Bienvenido' in response.data
    
    def test_failed_login_wrong_password(self, client, admin_user):
        """Probar login fallido con contraseña incorrecta"""
        response = client.post('/auth/login', data={
            'email': 'admin@test.com',
            'password': 'wrongpassword',
            'csrf_token': 'test'
        })
        
        assert response.status_code == 200
        assert 'Email o contraseña incorrectos'.encode('utf-8') in response.data
    
    def test_failed_login_nonexistent_user(self, client):
        """Probar login fallido con usuario inexistente"""
        response = client.post('/auth/login', data={
            'email': 'nonexistent@test.com',
            'password': 'password',
            'csrf_token': 'test'
        })
        
        assert response.status_code == 200
        assert 'Email o contraseña incorrectos'.encode('utf-8') in response.data
    
    def test_login_inactive_user(self, client, app):
        """Probar login con usuario inactivo"""
        with app.app_context():
            admin_role = Role.query.filter_by(name='admin').first()
            user = User(
                email='inactive@test.com',
                nombre='Inactive',
                apellido='User',
                role=admin_role,
                is_active=False
            )
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        response = client.post('/auth/login', data={
            'email': 'inactive@test.com',
            'password': 'password123',
            'csrf_token': 'test'
        })
        
        assert response.status_code == 200
        assert 'Tu cuenta está desactivada'.encode('utf-8') in response.data
    
    def test_successful_registration(self, client, app):
        """Probar registro exitoso"""
        with app.app_context():
            doctor_role = Role.query.filter_by(name='doctor').first()
            
            response = client.post('/auth/registro', data={
                'email': 'newuser@test.com',
                'nombre': 'New',
                'apellido': 'User',
                'role_id': doctor_role.id,
                'password': 'password123',
                'password2': 'password123',
                'csrf_token': 'test'
            }, follow_redirects=True)
            
            assert response.status_code == 200
            assert 'Registro exitoso'.encode('utf-8') in response.data
            
            # Verificar que el usuario fue creado
            user = User.query.filter_by(email='newuser@test.com').first()
            assert user is not None
            assert user.nombre == 'New'
            assert user.apellido == 'User'
    
    def test_registration_duplicate_email(self, client, admin_user, app):
        """Probar registro con email duplicado"""
        with app.app_context():
            doctor_role = Role.query.filter_by(name='doctor').first()
            
            response = client.post('/auth/registro', data={
                'email': 'admin@test.com',  # Email ya existe
                'nombre': 'Duplicate',
                'apellido': 'User',
                'role_id': doctor_role.id,
                'password': 'password123',
                'password2': 'password123',
                'csrf_token': 'test'
            })
            
            assert response.status_code == 200
            assert 'Este email ya está registrado'.encode('utf-8') in response.data
    
    def test_logout(self, client, admin_user):
        """Probar logout"""
        # Primero hacer login
        client.post('/auth/login', data={
            'email': 'admin@test.com',
            'password': 'admin123',
            'csrf_token': 'test'
        })
        
        # Luego hacer logout
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
        assert 'Has cerrado sesión correctamente'.encode('utf-8') in response.data

class TestMainViews:
    """Tests para las vistas principales"""
    
    def test_index_redirect_to_login(self, client):
        """Probar que index redirige a login cuando no autenticado"""
        response = client.get('/')
        assert response.status_code == 302
        assert '/auth/login' in response.headers['Location']
    
    def test_dashboard_requires_login(self, client):
        """Probar que dashboard requiere autenticación"""
        response = client.get('/dashboard')
        assert response.status_code == 302
        assert '/auth/login' in response.headers['Location']
    
    def test_dashboard_accessible_when_logged_in(self, client, admin_user):
        """Probar que dashboard es accesible cuando está logueado"""
        with client.session_transaction() as sess:
            sess['_user_id'] = str(admin_user.id)
            sess['_fresh'] = True
        
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'Bienvenido' in response.data
    
    def test_usuarios_admin_only(self, client, doctor_user):
        """Probar que página de usuarios es solo para admin"""
        with client.session_transaction() as sess:
            sess['_user_id'] = str(doctor_user.id)
            sess['_fresh'] = True
        
        response = client.get('/usuarios')
        assert response.status_code == 302  # Redirige por falta de permisos
    
    def test_usuarios_accessible_for_admin(self, client, admin_user):
        """Probar que página de usuarios es accesible para admin"""
        with client.session_transaction() as sess:
            sess['_user_id'] = str(admin_user.id)
            sess['_fresh'] = True
        
        response = client.get('/usuarios')
        assert response.status_code == 200
        assert b'Usuarios del Sistema' in response.data
    
    def test_perfil_accessible_when_logged_in(self, client, admin_user):
        """Probar que perfil es accesible cuando está logueado"""
        with client.session_transaction() as sess:
            sess['_user_id'] = str(admin_user.id)
            sess['_fresh'] = True
        
        response = client.get('/perfil')
        assert response.status_code == 200
        assert b'Mi Perfil' in response.data