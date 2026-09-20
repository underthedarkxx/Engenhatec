from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from ..models.user import User
from ..utils.responses import buscar_resposta
import random

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# Rota genérica que responde mensagens com respostas aleatórias
@chat_bp.route('', methods=['POST'])
@jwt_required()
def chat():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    if not user.is_subscribed:
        return jsonify({
            "error": "Acesso restrito a assinantes. Por favor, assine nosso serviço."
        }), 403

    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Mensagem é obrigatória"}), 400

    responses = [
        "Obrigado pela sua mensagem! Nossa equipe responderá em breve.",
        "Recebemos sua dúvida. Estamos verificando as informações.",
        "Mensagem registrada com sucesso!",
        "Em que mais podemos ajudar?",
        "Para essa pergunta, recomendamos verificar a seção de materiais relacionados."
    ]

    return jsonify({
        "reply": random.choice(responses),
        "original_message": data['message']
    }), 200


# Nova rota para responder perguntas com base no FAQ
@chat_bp.route('/perguntar', methods=['POST'])
@jwt_required()
def perguntar():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    if not user.is_subscribed:
        return jsonify({
            "error": "Acesso restrito a assinantes. Por favor, assine nosso serviço."
        }), 403

    data = request.get_json()
    pergunta = data.get('pergunta', '').strip()

    claims = get_jwt()
    username = claims.get('username', 'usuário')

    if not pergunta:
        return jsonify({"reply": "Por favor, envie uma pergunta."}), 400

    resposta = buscar_resposta(pergunta)

    if resposta:
        texto_resposta = f"✅ Bem-vindo ao chat, {username}!\n{pergunta}\n{resposta}"
    else:
        texto_resposta = f"✅ Bem-vindo ao chat, {username}!\n{pergunta}\nRecebemos sua dúvida. Estamos verificando as informações."

    return jsonify({"reply": texto_resposta}), 200


def init_chat_routes(app):
    app.register_blueprint(chat_bp)
