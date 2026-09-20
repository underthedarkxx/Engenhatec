from flask import jsonify
from backend.utils.material_faq import faq_materiais

def make_response(data=None, message=None, status=200):
    payload = {}
    if data is not None:
        payload['data'] = data
    if message is not None:
        payload['message'] = message
    return jsonify(payload), status

def buscar_resposta(pergunta):
    pergunta = pergunta.lower().strip()
    for item in faq_materiais:
        if pergunta in item['pergunta'].lower():
            return item['resposta']
    return "Desculpe, não encontrei uma resposta para essa pergunta."

