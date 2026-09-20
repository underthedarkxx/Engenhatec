from flask import render_template
from .auth import init_auth_routes
from .chat import init_chat_routes
from .materials import init_material_routes

def init_all_routes(app):
    init_auth_routes(app)
    init_material_routes(app)
    init_chat_routes(app)

    @app.route("/")
    def index():
        return render_template("index.html")
    
    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/register")
    def register():
        return render_template("register.html")
