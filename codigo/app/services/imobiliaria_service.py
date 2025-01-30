from flask import jsonify
from services.notificacao_service import NotificacaoService
from models import Imovel, Vistoria
from database import db

class ImobiliariaService:
    @staticmethod
    def desativar_imovel(id, data):
        # Busca o imóvel no banco de dados
        imovel = Imovel.query.get(data.get("imovel_id"))
        if not imovel:
            return jsonify({"error": "Imóvel não encontrado."}), 404

        # Atualiza o status do imóvel
        imovel.status = "desativado"
        db.session.commit()

        # Envia uma notificação
        mensagem = f"O imóvel {imovel.id} foi desativado pela imobiliária {id}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=imovel.proprietario_id)

        return jsonify({"message": "Imóvel desativado com sucesso.", "imovel": imovel.to_dict()}), 200

    @staticmethod
    def ativar_imovel(id, data):
        # Busca o imóvel no banco de dados
        imovel = Imovel.query.get(data.get("imovel_id"))
        if not imovel:
            return jsonify({"error": "Imóvel não encontrado."}), 404

        # Atualiza o status do imóvel
        imovel.status = "ativo"
        db.session.commit()

        # Envia uma notificação
        mensagem = f"O imóvel {imovel.id} foi ativado pela imobiliária {id}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=imovel.proprietario_id)

        return jsonify({"message": "Imóvel ativado com sucesso.", "imovel": imovel.to_dict()}), 200

    @staticmethod
    def cancelar_vistoria(id, data):
        # Busca a vistoria no banco de dados
        vistoria = Vistoria.query.get(data.get("vistoria_id"))
        if not vistoria:
            return jsonify({"error": "Vistoria não encontrada."}), 404

        # Remove a vistoria do banco
        db.session.delete(vistoria)
        db.session.commit()

        # Envia uma notificação
        mensagem = f"A vistoria {vistoria.id} foi cancelada pela imobiliária {id}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=vistoria.vistoriador_id)

        return jsonify({"message": "Vistoria cancelada com sucesso."}), 200
