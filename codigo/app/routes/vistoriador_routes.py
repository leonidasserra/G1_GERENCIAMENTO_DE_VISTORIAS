from flask import Blueprint, request, jsonify
from services.vistoriador_service import VistoriadorService

vistoriador_bp = Blueprint('vistoriador', __name__)

@vistoriador_bp.route('/vistoriador/<int:id>/registrar_inspecao', methods=['POST'])
def registrar_inspecao(id):
    try:
        # Validação dos dados recebidos
        data = request.json
        if not data or not all(key in data for key in ["vistoria_id", "texto", "fotos"]):
            return jsonify({"error": "Os campos 'vistoria_id', 'texto' e 'fotos' são obrigatórios."}), 400

        return VistoriadorService.registrar_inspecao(id, data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500
