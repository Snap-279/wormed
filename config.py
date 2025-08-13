"""
Configuración de la aplicación Flask Wormed
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de base de datos
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///wormed.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    
    # Configuración de admin por defecto
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL') or 'admin@wormed.local'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'
    
    # Configuración de seguridad
    WTF_CSRF_ENABLED = True
    
class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///wormed_dev.db'

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql://wormed_user:wormed_pass@localhost/wormed'

# Configuraciones disponibles
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}