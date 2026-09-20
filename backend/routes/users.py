from flask import Blueprint, jsonify
from backend.models.user import User  # import seu model User
from backend.extensions import db      # import da extensão db (SQLAlchemy)

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = []

    for user in users:
        users_list.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_subscribed': user.is_subscribed  # ajuste conforme seu campo real
        })
    return jsonify(users_list)
