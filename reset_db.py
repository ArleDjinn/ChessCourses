from app import create_app, db
from app.models import User, Course, Purchase  # importa todos tus modelos

app = create_app()

with app.app_context():
    # Elimina y recrea todas las tablas
    db.drop_all()
    db.create_all()
    print("Base de datos reiniciada correctamente.")
