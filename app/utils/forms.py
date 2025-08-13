"""
Formularios de la aplicación Wormed usando Flask-WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User, Role

class LoginForm(FlaskForm):
    """Formulario de inicio de sesión"""
    email = StringField('Email', validators=[
        DataRequired(message='El email es requerido'),
        Email(message='Email inválido')
    ], render_kw={
        'placeholder': 'tu@email.com',
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    })
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es requerida')
    ], render_kw={
        'placeholder': 'Tu contraseña',
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    })
    
    remember_me = BooleanField('Recordarme', render_kw={
        'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'
    })
    
    submit = SubmitField('Iniciar Sesión', render_kw={
        'class': 'w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
    })

class RegistroForm(FlaskForm):
    """Formulario de registro de usuario"""
    email = StringField('Email', validators=[
        DataRequired(message='El email es requerido'),
        Email(message='Email inválido')
    ], render_kw={
        'placeholder': 'tu@email.com',
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    })
    
    nombre = StringField('Nombre', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(min=2, max=64, message='El nombre debe tener entre 2 y 64 caracteres')
    ], render_kw={
        'placeholder': 'Tu nombre',
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    })
    
    apellido = StringField('Apellido', validators=[
        DataRequired(message='El apellido es requerido'),
        Length(min=2, max=64, message='El apellido debe tener entre 2 y 64 caracteres')
    ], render_kw={
        'placeholder': 'Tu apellido',
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    })
    
    role_id = SelectField('Rol', coerce=int, validators=[
        DataRequired(message='Debes seleccionar un rol')
    ], render_kw={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    })
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es requerida'),
        Length(min=6, message='La contraseña debe tener al menos 6 caracteres')
    ], render_kw={
        'placeholder': 'Mínimo 6 caracteres',
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    })
    
    password2 = PasswordField('Confirmar Contraseña', validators=[
        DataRequired(message='Debes confirmar la contraseña'),
        EqualTo('password', message='Las contraseñas deben coincidir')
    ], render_kw={
        'placeholder': 'Confirma tu contraseña',
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    })
    
    submit = SubmitField('Registrar', render_kw={
        'class': 'w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500'
    })
    
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        # Cargar roles disponibles
        self.role_id.choices = [(role.id, role.description) for role in Role.query.all()]
    
    def validate_email(self, email):
        """Validar que el email no esté en uso"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email ya está registrado. Usa otro email.')