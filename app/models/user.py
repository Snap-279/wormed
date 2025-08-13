"""
Modelos de usuario y rol para autenticación
"""
from datetime import datetime
from flask_login import UserMixin
from app import db

class Role(db.Model):
    """Modelo de rol de usuario"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con usuarios
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return f'<Role {self.name}>'
    
    @staticmethod
    def get_or_create_default_roles():
        """Crear roles por defecto del sistema"""
        roles = [
            {'name': 'admin', 'description': 'Administrador del sistema con acceso completo'},
            {'name': 'doctor', 'description': 'Doctor con acceso a notas clínicas'}
        ]
        
        for role_data in roles:
            role = Role.query.filter_by(name=role_data['name']).first()
            if not role:
                role = Role(**role_data)
                db.session.add(role)
        
        db.session.commit()
        return Role.query.all()

class User(UserMixin, db.Model):
    """Modelo de usuario del sistema"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    nombre = db.Column(db.String(64), nullable=False)
    apellido = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relación con rol
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    @property
    def nombre_completo(self):
        """Devuelve el nombre completo del usuario"""
        return f"{self.nombre} {self.apellido}"
    
    def has_role(self, role_name):
        """Verifica si el usuario tiene un rol específico"""
        return self.role and self.role.name == role_name
    
    def is_admin(self):
        """Verifica si el usuario es administrador"""
        return self.has_role('admin')
    
    def is_doctor(self):
        """Verifica si el usuario es doctor"""
        return self.has_role('doctor')
    
    def check_password(self, password):
        """Verifica la contraseña del usuario"""
        from app.utils.auth import check_password
        return check_password(password, self.password_hash)
    
    def set_password(self, password):
        """Establece la contraseña hasheada"""
        from app.utils.auth import hash_password
        self.password_hash = hash_password(password)
    
    def update_last_login(self):
        """Actualiza la fecha del último login"""
        self.last_login = datetime.utcnow()
        db.session.commit()