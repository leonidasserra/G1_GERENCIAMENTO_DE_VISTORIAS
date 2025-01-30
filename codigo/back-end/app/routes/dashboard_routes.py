from flask import Blueprint, request, jsonify
from services.dashboard_service import DashboardService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/vistorias', methods=['GET'])
def listar_vistorias():
    try:
        # Validação de parâmetros
        pagina = request.args.get("pagina", 1, type=int)
        limite = request.args.get("limite", 10, type=int)

        if pagina <= 0 or limite <= 0:
            return jsonify({"error": "Os parâmetros 'pagina' e 'limite' devem ser maiores que zero."}), 400

        return DashboardService.listar_vistorias({"pagina": pagina, "limite": limite})
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500
