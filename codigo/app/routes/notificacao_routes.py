from flask import Blueprint, request, jsonify
from services.notificacao_service import NotificacaoService

notificacao_bp = Blueprint('notificacao', __name__)

@notificacao_bp.route('/notificacoes', methods=['GET'])
def listar_notificacoes():
    try:
        # Validação do parâmetro destinatario_id
        destinatario_id = request.args.get("destinatario_id", type=int)
        if not destinatario_id:
            return jsonify({"error": "O parâmetro 'destinatario_id' é obrigatório e deve ser um número inteiro."}), 400

        return NotificacaoService.listar_notificacoes(destinatario_id)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500

@notificacao_bp.route('/notificacoes/<int:id>', methods=['PUT'])
def marcar_como_lida(id):
    try:
        return NotificacaoService.marcar_como_lida(id)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500