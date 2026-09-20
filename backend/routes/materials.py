from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from ..models.material import Material
from .. import db
from ..utils.material_faq import faq_materiais  # Importando as perguntas frequentes

materials_bp = Blueprint('materials_bp', __name__, url_prefix='/materials')


@materials_bp.route('', methods=['GET'])
@jwt_required()
def get_materials():
    materials = Material.query.all()
    return jsonify([material.to_dict() for material in materials]), 200

@materials_bp.route('/<int:material_id>', methods=['GET'])
@jwt_required()
def get_material(material_id):
    material = Material.query.get_or_404(material_id)
    return jsonify(material.to_dict()), 200

@materials_bp.route('', methods=['POST'])
@jwt_required()
def create_material():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Dados inválidos"}), 400

    new_material = Material(
        name=data['name'],
        image_url=data.get('image_url'),
        caption=data.get('caption'),
        description=data.get('description'),
        category=data.get('category')
    )

    db.session.add(new_material)
    db.session.commit()

    return jsonify({
        "message": "Material criado com sucesso",
        "material": new_material.to_dict()
    }), 201

@materials_bp.route('/<int:material_id>', methods=['PUT'])
@jwt_required()
def update_material(material_id):
    material = Material.query.get_or_404(material_id)
    data = request.get_json()
    if 'name' in data:
        material.name = data['name']
    if 'image_url' in data:
        material.image_url = data['image_url']
    if 'caption' in data:
        material.caption = data['caption']
    if 'description' in data:
        material.description = data['description']
    if 'category' in data:
        material.category = data['category']

    db.session.commit()

    return jsonify({
        "message": "Material atualizado com sucesso",
        "material": material.to_dict()
    }), 200

@materials_bp.route('/<int:material_id>', methods=['DELETE'])
@jwt_required()
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()

    return jsonify({"message": "Material deletado com sucesso"}), 200

# ✅ Nova rota: FAQ para assinantes
@materials_bp.route('/faq', methods=['GET'])
@jwt_required()
def get_material_faq():
    claims = get_jwt()
    if not claims.get("is_subscribed", False):
        return jsonify({"error": "Acesso permitido apenas para assinantes"}), 403
    
    return jsonify(faq_materiais), 200

def init_material_routes(app):
    app.register_blueprint(materials_bp)

