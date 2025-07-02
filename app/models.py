from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    purchases = db.relationship('Purchase', back_populates='user')

class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False)

    precio = db.Column(db.Integer, nullable=False)
    precio_descuento = db.Column(db.Integer, nullable=True)  # Opcional si está en oferta
    en_oferta = db.Column(db.Boolean, default=False)

    imagen = db.Column(db.String(255), nullable=True)  # Ruta relativa dentro de /static
    categoria = db.Column(db.String(100), nullable=True)

    url_video = db.Column(db.String(255), nullable=False)  # Video principal del curso
    activo = db.Column(db.Boolean, default=True)

    fecha_creacion = db.Column(db.DateTime, default=db.func.now())

    purchases = db.relationship('Purchase', back_populates='course')


class Purchase(db.Model):
    __tablename__ = 'purchase'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    user = db.relationship('User', back_populates='purchases')
    course = db.relationship('Course', back_populates='purchases')
