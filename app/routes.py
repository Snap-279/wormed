from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from . import db
from .models import User, Patient, Task, ClinicalNote, Attachment

main = Blueprint('main', __name__, template_folder='templates')

@main.route('/health')
def health():
    return {"status": "ok"}

@main.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception:
        return "¡Bienvenido a Wormed!"

# ---------- USUARIOS ----------
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name  = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', 'changeme')
        if not name or not email:
            flash('Nombre y email son requeridos.', 'warning')
            return redirect(url_for('main.register'))
        try:
            u = User(name=name, email=email, password=password)
            db.session.add(u)
            db.session.commit()
            flash('Usuario creado.', 'success')
            return redirect(url_for('main.list_users'))
        except IntegrityError:
            db.session.rollback()
            flash('Ese email ya existe.', 'danger')
            return redirect(url_for('main.register'))
    # GET
    try:
        return render_template('register.html')
    except Exception:
        return """
        <h1>Registro</h1>
        <form method="post">
          <input name="name" placeholder="Nombre" required><br>
          <input name="email" type="email" placeholder="Email" required><br>
          <input name="password" type="password" placeholder="Password"><br>
          <button type="submit">Crear</button>
        </form>
        """

@main.route('/users')
def list_users():
    users = User.query.all()
    try:
        return render_template('users.html', users=users)
    except Exception:
        items = "".join(f"<li>{u.id} — {u.name} — {u.email}</li>" for u in users) or "<li>Sin usuarios</li>"
        return f"<h1>Usuarios</h1><ul>{items}</ul>"

# ---------- PACIENTES ----------
@main.route('/patients')
def patient_list():
    try:
        patients = Patient.query.order_by(Patient.last_name).all()
    except Exception:
        patients = Patient.query.all()
    try:
        return render_template('patients.html', patients=patients)
    except Exception:
        items = "".join(
            f"<li>{p.id} — {getattr(p,'last_name','')} {getattr(p,'first_name','')} (MRN: {getattr(p,'mrn','')})</li>"
            for p in patients
        ) or "<li>Sin pacientes</li>"
        return f"<h1>Pacientes</h1><ul>{items}</ul>"

@main.route('/patients/<int:patient_id>')
def patient_detail(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('patient_detail.html', patient=patient)

@main.route('/patients/<int:patient_id>/edit', methods=['GET', 'POST'])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip() or patient.first_name
        last_name = request.form.get('last_name', '').strip() or patient.last_name
        mrn = request.form.get('mrn', '').strip() or patient.mrn
        patient.first_name = first_name
        patient.last_name = last_name
        patient.mrn = mrn
        try:
            db.session.commit()
            flash('Paciente actualizado.', 'success')
            return redirect(url_for('main.patient_detail', patient_id=patient.id))
        except IntegrityError:
            db.session.rollback()
            flash('Error al actualizar el paciente.', 'danger')
    try:
        return render_template('patient_edit.html', patient=patient)
    except Exception:
        return f"""
        <h1>Editar Paciente</h1>
        <form method="post">
          <input name="first_name" placeholder="Nombre" value="{patient.first_name or ''}"><br>
          <input name="last_name" placeholder="Apellido" value="{patient.last_name or ''}"><br>
          <input name="mrn" placeholder="MRN" value="{patient.mrn or ''}"><br>
          <button type="submit">Actualizar</button>
        </form>
        """

# ---------- TAREAS ----------
@main.route('/tasks')
def task_list():
    try:
        tasks = Task.query.order_by(Task.created_at.desc()).all()
    except Exception:
        tasks = Task.query.all()
    try:
        return render_template('tasks.html', tasks=tasks)
    except Exception:
        items = "".join(
            f"<li>{t.id} — {t.title} — {t.status} — patient_id={t.patient_id}</li>"
            for t in tasks
        ) or "<li>Sin tareas</li>"
        return f"<h1>Tareas</h1><ul>{items}</ul>"
