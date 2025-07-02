from app import create_app, db
from app.models import Course

app = create_app()

def prompt_input(campo, obligatorio=True, tipo=str, default=None):
    while True:
        entrada = input(f"{campo}{' [' + str(default) + ']' if default else ''}: ").strip()
        if not entrada and default is not None:
            return default
        if not entrada and obligatorio:
            print("Este campo es obligatorio.")
            continue
        try:
            return tipo(entrada)
        except ValueError:
            print(f"Entrada inválida. Esperaba un valor tipo {tipo.__name__}.")

def crear_curso():
    print("\n📚 Crear nuevo curso")
    titulo = prompt_input("Título")
    descripcion = prompt_input("Descripción")
    slug = prompt_input("Slug (url amigable, sin espacios)")
    precio = prompt_input("Precio CLP", tipo=int)
    tiene_descuento = prompt_input("¿Está en oferta? (s/n)", tipo=str, default="n").lower() == "s"
    precio_descuento = prompt_input("Precio con descuento", tipo=int) if tiene_descuento else None
    imagen = prompt_input("Ruta imagen (ej: images/cursos/aperturas.jpg)")
    categoria = prompt_input("Categoría (ej: Táctica, Finales, Aperturas)")
    url_video = prompt_input("URL del video (ej: https://...)")
    activo = prompt_input("¿Curso activo? (s/n)", tipo=str, default="s").lower() == "s"

    curso = Course(
        titulo=titulo,
        descripcion=descripcion,
        slug=slug,
        precio=precio,
        precio_descuento=precio_descuento,
        en_oferta=tiene_descuento,
        imagen=imagen,
        categoria=categoria,
        url_video=url_video,
        activo=activo
    )
    db.session.add(curso)
    db.session.commit()
    print(f"✅ Curso '{titulo}' guardado correctamente.")

if __name__ == '__main__':
    app.app_context().push()
    print("👋 Bienvenido al generador de cursos\n")
    while True:
        crear_curso()
        continuar = input("\n¿Deseas ingresar otro curso? (s/n): ").strip().lower()
        if continuar != "s":
            print("👋 Fin del ingreso de cursos.")
            break
