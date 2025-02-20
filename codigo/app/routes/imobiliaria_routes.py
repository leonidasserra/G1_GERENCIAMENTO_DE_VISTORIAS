from flask import Blueprint, request, jsonify
from services.imobiliaria_service import ImobiliariaService
from models import Imovel  # Modelo de imóveis
from utils.decorators import autorizacao_permitida

imobiliaria_bp = Blueprint('imobiliaria', __name__)

@imobiliaria_bp.route('/imobiliaria/<int:id>/desativar_imovel', methods=['PUT'])
@autorizacao_permitida(["Imobiliaria"])  # Apenas Imobiliarias podem acessar
def desativar_imovel(id):
    """
    Desativa um imóvel específico.
    """
    try:
        data = request.json
        if not data or "imovel_id" not in data:
            return jsonify({"error": "O campo 'imovel_id' é obrigatório."}), 400

        return ImobiliariaService.desativar_imovel(id, data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500


@imobiliaria_bp.route('/imobiliaria/<int:id>/ativar_imovel', methods=['PUT'])
@autorizacao_permitida(["Imobiliaria"])  # Apenas Imobiliarias podem acessar
def ativar_imovel(id):
    """
    Ativa um imóvel específico.
    """
    try:
        data = request.json
        if not data or "imovel_id" not in data:
            return jsonify({"error": "O campo 'imovel_id' é obrigatório."}), 400

        return ImobiliariaService.ativar_imovel(id, data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500


@imobiliaria_bp.route('/imobiliaria/<int:id>/cancelar_vistoria', methods=['PUT'])
@autorizacao_permitida(["Imobiliaria"])  # Apenas Imobiliarias podem acessar
def cancelar_vistoria(id):
    """
    Cancela uma vistoria específica.
    """
    try:
        data = request.json
        if not data or "vistoria_id" not in data:
            return jsonify({"error": "O campo 'vistoria_id' é obrigatório."}), 400

        return ImobiliariaService.cancelar_vistoria(id, data)
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500


@imobiliaria_bp.route('/imobiliaria/imoveis', methods=['GET'])
@autorizacao_permitida(["Imobiliaria"])  # Apenas Imobiliarias podem acessar
def listar_imoveis():
    """
    Lista os imóveis cadastrados com filtros opcionais.
    """
    try:
        # Filtros opcionais
        status = request.args.get("status")  # Exemplo: "Ativo", "Desativado"
        tipo = request.args.get("tipo")  # Exemplo: "Casa", "Apartamento"
        pagina = int(request.args.get("pagina", 1))
        limite = int(request.args.get("limite", 10))
        offset = (pagina - 1) * limite

        # Consulta ao banco de dados com filtros e paginação
        query = Imovel.query
        if status:
            query = query.filter_by(status=status)
        if tipo:
            query = query.filter_by(tipo=tipo)

        total = query.count()
        imoveis = query.offset(offset).limit(limite).all()

        # Formatar a resposta
        response = {
            "pagina": pagina,
            "limite": limite,
            "total_imoveis": total,
            "imoveis": [imovel.to_dict() for imovel in imoveis]
        }

        return jsonify({"message": "Imóveis listados com sucesso.", "dados": response}), 200
    except Exception as e:
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500
