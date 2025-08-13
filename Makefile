# Makefile para el proyecto Wormed
# Sistema de Gestión Clínica con Flask

.PHONY: help install dev test clean migrate upgrade downgrade create-admin shell lint format docker docker-dev

# Variables
PYTHON = python3
PIP = pip
FLASK_APP = app.py
FLASK_ENV = development

# Help
help:
	@echo "Comandos disponibles para Wormed:"
	@echo ""
	@echo "  Desarrollo:"
	@echo "    install     - Instalar dependencias"
	@echo "    dev         - Iniciar servidor de desarrollo"
	@echo "    shell       - Abrir shell Flask interactivo"
	@echo ""
	@echo "  Base de datos:"
	@echo "    migrate     - Crear nueva migración"
	@echo "    upgrade     - Aplicar migraciones a la BD"
	@echo "    downgrade   - Revertir última migración"
	@echo "    create-admin - Crear usuario administrador"
	@echo ""
	@echo "  Testing y calidad:"
	@echo "    test        - Ejecutar tests"
	@echo "    lint        - Verificar código con flake8"
	@echo "    format      - Formatear código con black"
	@echo ""
	@echo "  Docker:"
	@echo "    docker      - Construir imagen Docker"
	@echo "    docker-dev  - Ejecutar con docker-compose"
	@echo ""
	@echo "  Utilidades:"
	@echo "    clean       - Limpiar archivos temporales"

# Instalación de dependencias
install:
	@echo "Instalando dependencias..."
	$(PIP) install --break-system-packages -r requirements.txt
	@echo "✅ Dependencias instaladas"

# Desarrollo
dev: export FLASK_APP=$(FLASK_APP)
dev: export FLASK_ENV=$(FLASK_ENV)
dev: export PATH := $(PATH):/home/ubuntu/.local/bin
dev:
	@echo "🚀 Iniciando servidor de desarrollo..."
	@echo "Aplicación disponible en: http://localhost:5000"
	@echo "Usuario admin: admin@wormed.local / admin123"
	flask run --host=0.0.0.0 --debug

# Shell interactivo
shell: export FLASK_APP=$(FLASK_APP)
shell: export PATH := $(PATH):/home/ubuntu/.local/bin
shell:
	@echo "🐚 Abriendo shell Flask..."
	flask shell

# Base de datos - Crear migración
migrate: export FLASK_APP=$(FLASK_APP)
migrate: export PATH := $(PATH):/home/ubuntu/.local/bin
migrate:
	@echo "📋 Creando nueva migración..."
	@read -p "Mensaje de migración: " msg; \
	flask db migrate -m "$$msg"

# Base de datos - Aplicar migraciones
upgrade: export FLASK_APP=$(FLASK_APP)
upgrade: export PATH := $(PATH):/home/ubuntu/.local/bin
upgrade:
	@echo "⬆️  Aplicando migraciones..."
	flask db upgrade
	@echo "✅ Base de datos actualizada"

# Base de datos - Revertir migración
downgrade: export FLASK_APP=$(FLASK_APP)
downgrade: export PATH := $(PATH):/home/ubuntu/.local/bin
downgrade:
	@echo "⬇️  Revirtiendo última migración..."
	flask db downgrade
	@echo "✅ Migración revertida"

# Crear usuario administrador
create-admin: export FLASK_APP=$(FLASK_APP)
create-admin: export PATH := $(PATH):/home/ubuntu/.local/bin
create-admin:
	@echo "👑 Creando usuario administrador..."
	flask create-admin
	@echo "✅ Usuario admin listo"

# Tests
test: export PATH := $(PATH):/home/ubuntu/.local/bin
test:
	@echo "🧪 Ejecutando tests..."
	$(PYTHON) -m pytest tests/ -v --tb=short
	@echo "✅ Tests completados"

# Tests con cobertura
test-cov: export PATH := $(PATH):/home/ubuntu/.local/bin
test-cov:
	@echo "🧪 Ejecutando tests con cobertura..."
	$(PYTHON) -m pytest tests/ -v --cov=app --cov-report=html --cov-report=term
	@echo "✅ Tests completados - ver htmlcov/index.html"

# Linting
lint:
	@echo "🔍 Verificando código..."
	flake8 app tests --max-line-length=88 --exclude=migrations
	@echo "✅ Código verificado"

# Formateo
format:
	@echo "🎨 Formateando código..."
	black app tests --line-length=88
	@echo "✅ Código formateado"

# Docker - Construir imagen
docker:
	@echo "🐳 Construyendo imagen Docker..."
	docker build -t wormed:latest .
	@echo "✅ Imagen Docker creada"

# Docker - Desarrollo con compose
docker-dev:
	@echo "🐳 Iniciando con docker-compose..."
	docker-compose up --build
	@echo "✅ Servicios levantados"

# Limpiar archivos temporales
clean:
	@echo "🧹 Limpiando archivos temporales..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage
	@echo "✅ Archivos temporales eliminados"

# Setup inicial completo
setup: install upgrade create-admin
	@echo ""
	@echo "🎉 ¡Wormed configurado exitosamente!"
	@echo ""
	@echo "Para iniciar el desarrollo ejecuta:"
	@echo "  make dev"
	@echo ""
	@echo "Credenciales por defecto:"
	@echo "  Email: admin@wormed.local"
	@echo "  Password: admin123"
	@echo ""

# Verificar que todo funciona
check: lint test
	@echo "✅ Todas las verificaciones pasaron"

# Reset completo de la base de datos
reset-db: export FLASK_APP=$(FLASK_APP)
reset-db: export PATH := $(PATH):/home/ubuntu/.local/bin
reset-db:
	@echo "⚠️  ADVERTENCIA: Esto eliminará todos los datos"
	@read -p "¿Estás seguro? (y/N): " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		rm -f *.db; \
		rm -rf migrations/versions/*; \
		flask db init; \
		flask db migrate -m "Initial migration: User and Role models"; \
		flask db upgrade; \
		flask create-admin; \
		echo "✅ Base de datos reiniciada"; \
	else \
		echo "❌ Operación cancelada"; \
	fi