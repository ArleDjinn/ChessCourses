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
    precio = db.Column(db.Integer, nullable=False)
    url_video = db.Column(db.String(255), nullable=False)
    purchases = db.relationship('Purchase', back_populates='course')
    slug = db.Column(db.String(150), unique=True, nullable=False)

class Purchase(db.Model):
    __tablename__ = 'purchase'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)

    user = db.relationship('User', back_populates='purchases')
    course = db.relationship('Course', back_populates='purchases')
