from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class RegisterForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrarse')

class FormularioContactoManual(FlaskForm):
    class Meta:
        csrf = False  # Desactivamos CSRF porque el formulario es AJAX
    widget_contact_form_name = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(max=100, message="Máximo 100 caracteres.")
        ]
    )
    widget_contact_form_email = StringField(
        "Correo",
        validators=[
            DataRequired(message="El correo es obligatorio."),
            Email(message="Correo inválido."),
            Length(max=120, message="Máximo 120 caracteres.")
        ]
    )
    widget_contact_form_message = TextAreaField(
        "Mensaje",
        validators=[
            DataRequired(message="El mensaje es obligatorio."),
            Length(max=1000, message="Máximo 1000 caracteres.")
        ]
    )