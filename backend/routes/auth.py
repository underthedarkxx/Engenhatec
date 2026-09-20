from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from ..models.user import User
from .. import db, bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data or 'email' not in data:
        return jsonify({"error": "Dados incompletos"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Nome de usuário já existe"}), 409

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email já cadastrado"}), 409

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        is_subscribed=data.get('is_subscribed', False)
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Usuário registrado com sucesso",
        "user": new_user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Credenciais necessárias"}), 400

    user = User.query.filter_by(username=data['username']).first()

    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"error": "Credenciais inválidas"}), 401

    additional_claims = {"is_subscribed": user.is_subscribed}
    
    # 🔧 Corrigido: transforme user.id em string
    access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)

    return jsonify({
        "message": "Login bem-sucedido",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200


# Rota nova para retornar os dados do usuário autenticado
@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    claims = get_jwt()  # Pega os claims do token (ex: is_subscribed)

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_subscribed": claims.get('is_subscribed', False)  # Pode pegar direto do token
    }), 200


def init_auth_routes(app):
    app.register_blueprint(auth_bp)
