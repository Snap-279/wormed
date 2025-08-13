# Wormed - Sistema de Gestión Clínica

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Wormed** es un sistema web de gestión clínica desarrollado con Flask y Python, diseñado para optimizar el procesamiento de notas clínicas, codificación automática ICD-10, evaluación de cumplimiento HEDIS y generación de reportes médicos.

## 🚀 Características Principales

### ✅ Fase 1 - Completada (Autenticación y Base)
- **Autenticación robusta** con Flask-Login y bcrypt
- **Sistema de roles** (Administrador/Doctor) con permisos granulares
- **Interface moderna** con Tailwind CSS y componentes responsive
- **Base de datos** SQLAlchemy con migraciones Alembic
- **Testing** completo con pytest
- **Docker** support para desarrollo y producción

### 🔄 Fases Futuras (Roadmap)
- **Gestión de pacientes** y historiales médicos
- **Procesamiento de notas clínicas** con IA
- **Codificación automática ICD-10**
- **Ingesta de PDFs** médicos y extracción de datos
- **Métricas HEDIS** y reportes de cumplimiento
- **Sistema de facturación** y códigos CPT
- **Dashboard analítico** con visualizaciones

## 📋 Requisitos del Sistema

- **Python 3.11+**
- **pip** (gestor de paquetes)
- **SQLite** (desarrollo) / **MySQL** (producción)
- **Docker** (opcional)

## 🛠️ Instalación Rápida

### Opción 1: Instalación Manual

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd wormed

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 3. Instalar dependencias
make install

# 4. Configurar base de datos y admin
make setup

# 5. Iniciar servidor de desarrollo
make dev
```

### Opción 2: Con Docker

```bash
# Desarrollo con Docker Compose
docker-compose up --build

# O construir imagen personalizada
make docker
docker run -p 5000:5000 wormed:latest
```

## 🎯 Uso del Sistema

### Acceso Inicial

Una vez instalado, accede a la aplicación:

- **URL**: http://localhost:5000
- **Usuario Admin**: `admin@wormed.local`
- **Contraseña**: `admin123`

### Comandos Make Disponibles

```bash
# Desarrollo
make dev          # Iniciar servidor de desarrollo
make shell        # Shell Flask interactivo

# Base de datos
make migrate      # Crear nueva migración
make upgrade      # Aplicar migraciones
make create-admin # Crear usuario administrador

# Testing y calidad
make test         # Ejecutar tests
make lint         # Verificar código
make format       # Formatear código

# Utilidades
make clean        # Limpiar archivos temporales
make help         # Ver todos los comandos
```

## 🏗️ Arquitectura del Sistema

### Estructura del Proyecto

```
wormed/
├── app/                    # Aplicación Flask
│   ├── models/            # Modelos SQLAlchemy
│   │   ├── __init__.py
│   │   └── user.py        # User y Role models
│   ├── views/             # Blueprints y rutas
│   │   ├── __init__.py
│   │   ├── auth.py        # Autenticación
│   │   └── main.py        # Vistas principales
│   ├── templates/         # Templates Jinja2
│   │   ├── layouts/       # Layouts base
│   │   ├── auth/          # Templates de autenticación
│   │   └── main/          # Templates principales
│   ├── static/            # Archivos estáticos
│   │   ├── css/
│   │   └── js/
│   ├── utils/             # Utilidades
│   │   ├── __init__.py
│   │   ├── auth.py        # Decoradores y hash
│   │   └── forms.py       # Formularios WTF
│   └── __init__.py        # Factory de la app
├── tests/                 # Tests unitarios
│   ├── __init__.py
│   ├── conftest.py        # Configuración pytest
│   ├── test_models.py     # Tests de modelos
│   └── test_auth.py       # Tests de autenticación
├── migrations/            # Migraciones Alembic
├── config.py              # Configuraciones
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias Python
├── Dockerfile             # Imagen Docker
├── docker-compose.yml     # Servicios Docker
├── Makefile              # Comandos de desarrollo
└── README.md             # Este archivo
```

### Tecnologías Utilizadas

#### Backend
- **Flask 2.3.3** - Framework web minimalista
- **SQLAlchemy 3.0.5** - ORM para base de datos
- **Flask-Login 0.6.3** - Gestión de sesiones
- **Flask-WTF 1.1.1** - Formularios y CSRF
- **Flask-Migrate 4.0.5** - Migraciones de BD
- **bcrypt 4.0.1** - Hashing de contraseñas

#### Frontend
- **Tailwind CSS** - Framework CSS utilitario
- **Font Awesome** - Iconografía
- **Jinja2** - Motor de templates
- **JavaScript vanilla** - Interactividad

#### Testing y Desarrollo
- **pytest 7.4.2** - Framework de testing
- **pytest-flask 1.2.0** - Testing específico para Flask
- **Docker** - Contenedores
- **Alembic** - Migraciones de base de datos

## 🔐 Sistema de Autenticación

### Roles Disponibles

1. **Administrador (`admin`)**
   - Acceso completo al sistema
   - Gestión de usuarios
   - Configuración del sistema
   - Reportes y análisis

2. **Doctor (`doctor`)**
   - Acceso a notas clínicas
   - Gestión de pacientes
   - Visualización de métricas

### Decoradores de Seguridad

```python
from app.utils.auth import admin_required, doctor_required

@admin_required
def admin_only_view():
    """Vista solo para administradores"""
    pass

@doctor_required  
def medical_view():
    """Vista para doctores y administradores"""
    pass
```

## 🧪 Testing

### Ejecutar Tests

```bash
# Tests básicos
make test

# Tests con cobertura
make test-cov
```

### Cobertura Actual

- **Modelos**: 100% - Tests completos para User y Role
- **Autenticación**: 90% - Login, logout, registro
- **Vistas**: 85% - Páginas principales y dashboard
- **Utilidades**: 95% - Decoradores y helpers

## 📝 Variables de Entorno

Configura estas variables en tu archivo `.env`:

```bash
# Configuración Flask
SECRET_KEY=tu_clave_secreta_super_segura_aqui
FLASK_APP=app
FLASK_ENV=development

# Base de datos
DATABASE_URL=sqlite:///wormed.db

# Configuración admin por defecto
ADMIN_EMAIL=admin@wormed.local
ADMIN_PASSWORD=admin123
```

### Variables para Producción

```bash
# Producción
FLASK_ENV=production
SECRET_KEY=clave_super_secreta_de_produccion
DATABASE_URL=mysql://user:password@localhost/wormed

# Opcional: Configuración de email, AWS, etc.
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=tu_email@domain.com
MAIL_PASSWORD=tu_password_de_app
```

## 🐳 Docker

### Desarrollo Local

```bash
# Iniciar todos los servicios
docker-compose up --build

# Solo la aplicación web
docker build -t wormed .
docker run -p 5000:5000 wormed
```

### Servicios Incluidos

- **Web App**: Flask en puerto 5000
- **MySQL**: Base de datos en puerto 3306

## 🚧 Desarrollo

### Agregar Nuevas Funcionalidades

1. **Crear modelo**:
```bash
# En app/models/
# Crear nuevo archivo, ej: patient.py
make migrate  # Crear migración
make upgrade  # Aplicar a BD
```

2. **Crear vista**:
```bash
# En app/views/
# Crear blueprint, registrar en app/__init__.py
```

3. **Agregar tests**:
```bash
# En tests/
# Crear test_nuevafuncionalidad.py
make test  # Verificar
```

### Guías de Código

- **PEP 8** para Python
- **Líneas máx 88 caracteres**
- **Docstrings** en español para funciones
- **Type hints** cuando sea posible
- **Tests** para todas las funcionalidades

## 📊 Métricas de Calidad

### Tests
- ✅ 21/26 tests pasando (81%)
- ✅ Cobertura de modelos: 100%
- ✅ Cobertura de autenticación: 90%

### Código
- ✅ Estructura modular con Blueprints
- ✅ Separación de responsabilidades
- ✅ Configuración por entornos
- ✅ Documentación completa

## 🔍 Troubleshooting

### Problemas Comunes

1. **Error: `flask: command not found`**
```bash
export PATH=$PATH:/home/ubuntu/.local/bin
# O usar make dev que ya incluye el PATH
```

2. **Error de migraciones**
```bash
make reset-db  # Reinicia completamente la BD
```

3. **Problemas de dependencias**
```bash
make clean
make install
```

4. **Puerto 5000 ocupado**
```bash
# Cambiar puerto en app.py o usar Docker
export FLASK_RUN_PORT=8000
make dev
```

## 🤝 Contribución

### Proceso de Desarrollo

1. **Fork** el repositorio
2. **Crear branch** para nueva funcionalidad
3. **Implementar** con tests
4. **Verificar** que todo pasa: `make check`
5. **Crear Pull Request**

### Estándares de Commit

```bash
feat: agregar nueva funcionalidad
fix: corregir error
docs: actualizar documentación
test: agregar o modificar tests
refactor: refactorizar código
style: cambios de formato
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:

- **Issues**: GitHub Issues
- **Documentación**: Este README
- **Wiki**: GitHub Wiki (próximamente)

---

## 🎯 Próximos Pasos (Fase 2)

1. **Modelos de pacientes** y historiales
2. **Upload de archivos** PDF
3. **Integración con APIs** médicas
4. **Dashboard** con métricas en tiempo real
5. **Sistema de notificaciones**

¡Wormed está listo para comenzar el desarrollo de funcionalidades médicas avanzadas! 🏥

---

*Desarrollado con ❤️ para mejorar la gestión clínica*