from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from .models import User, Purchase, Course, MensajeContacto
from .forms import RegisterForm, LoginForm, FormularioContactoManual
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Credenciales incorrectas')
    return render_template('login.html', form=form, hide_header=True)

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegisterForm()
    if form.validate_on_submit():
        user_existente = User.query.filter_by(email=form.email.data).first()
        if user_existente:
            flash('El correo ya está registrado.')
            return redirect(url_for('main.registro'))
        nuevo_usuario = User(
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Registro exitoso. Puedes iniciar sesión.')
        return redirect(url_for('main.login'))
    return render_template('registro.html', form=form, hide_header=True)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/mis_cursos')
@login_required
def mis_cursos():
    compras = Purchase.query.filter_by(user_id=current_user.id).all()
    lista_de_cursos = [compra.course for compra in compras]
    return render_template('mis_cursos.html', cursos=lista_de_cursos)

@main.route('/curso/<string:slug>')
def ver_curso(slug):
    curso = Course.query.filter_by(slug=slug).first_or_404()

    # Si el usuario está logueado, verificar si tiene acceso
    tiene_acceso = False
    if current_user.is_authenticated:
        tiene_acceso = any(compra.course_id == curso.id for compra in current_user.purchases)

    return render_template('curso.html', curso=curso, tiene_acceso=tiene_acceso)

@main.route('/comprar/<string:slug>', methods=['POST'])
@login_required
def comprar_curso(slug):
    curso = Course.query.filter_by(slug=slug).first_or_404()

    ya_comprado = Purchase.query.filter_by(user_id=current_user.id, course_id=curso.id).first()
    if ya_comprado:
        flash('Ya compraste este curso.')
        return redirect(url_for('main.ver_curso', slug=curso.slug))

    nueva_compra = Purchase(user_id=current_user.id, course_id=curso.id)
    db.session.add(nueva_compra)
    db.session.commit()
    flash('¡Curso comprado exitosamente!')
    return redirect(url_for('main.mis_cursos'))

@main.route('/cursos')
def cursos_disponibles():
    cursos = Course.query.all()
    return render_template('cursos.html', cursos=cursos)

@main.route('/buscar')
def buscar():
    consulta = request.args.get('q', '').strip()
    if consulta:
        resultados = Course.query.filter(
            Course.activo.is_(True),
            db.or_(
                Course.titulo.ilike(f'%{consulta}%'),
                Course.descripcion.ilike(f'%{consulta}%')
            )
        ).all()
    else:
        resultados = []
    return render_template('resultados_busqueda.html', consulta=consulta, resultados=resultados)


@main.route('/contacto', methods=['POST'])
def contacto():
    # Mapeamos manualmente los nombres del HTML a los que espera WTForms
    formdata = {
        "widget_contact_form_name": request.form.get("widget-contact-form-name"),
        "widget_contact_form_email": request.form.get("widget-contact-form-email"),
        "widget_contact_form_message": request.form.get("widget-contact-form-message"),
    }

    form = FormularioContactoManual(data=formdata)

    if form.validate():
        nuevo_mensaje = MensajeContacto(
            nombre=form.widget_contact_form_name.data,
            correo=form.widget_contact_form_email.data,
            mensaje=form.widget_contact_form_message.data
        )
        db.session.add(nuevo_mensaje)
        db.session.commit()

        return jsonify({
            "response": "success",
            "message": "Gracias por tu mensaje. Te contactaremos pronto."
        })

    return jsonify({
        "response": "error",
        "message": next(iter(form.errors.values()))[0]  # Primer error
    }), 400