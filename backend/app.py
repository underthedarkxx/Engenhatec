from . import create_app  # Importa do __init__.py do pacote backend

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

