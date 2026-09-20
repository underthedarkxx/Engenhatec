import os
from flask import Flask
from .extensions import db, jwt, bcrypt
from .config import config
from backend.routes.users import users_bp

def create_app(config_name='default'):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    templates_path = os.path.join(base_dir, '..', 'frontend', 'templates')
    static_path = os.path.join(base_dir, '..', 'frontend', 'static')

    app = Flask(
        __name__,
        template_folder=templates_path,
        static_folder=static_path
    )

    # Configurações
    app.config.from_object(config[config_name])

    # Extensões
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Registra Blueprints
    app.register_blueprint(users_bp)

    from .routes import init_all_routes
    init_all_routes(app)

    # Cria as tabelas no banco
    with app.app_context():
        db.create_all()

    return app



