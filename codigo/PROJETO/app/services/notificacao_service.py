from flask import jsonify
from datetime import datetime
from models import Notificacao
from database import db

class NotificacaoService:
    @staticmethod
    def criar_notificacao(mensagem, destinatario_id):
        """
        Cria uma nova notificação e a salva no banco de dados.
        """
        nova_notificacao = Notificacao(
            mensagem=mensagem,
            usuario_id=destinatario_id,
            data_criacao=datetime.utcnow(),
            lida=False
        )
        db.session.add(nova_notificacao)
        db.session.commit()

        return nova_notificacao.to_dict()

    @staticmethod
    def listar_notificacoes(destinatario_id):
        """
        Lista todas as notificações de um destinatário específico.
        """
        notificacoes = Notificacao.query.filter_by(usuario_id=destinatario_id).all()
        return jsonify([n.to_dict() for n in notificacoes]), 200

    @staticmethod
    def marcar_como_lida(id):
        """
        Marca uma notificação como lida.
        """
        notificacao = Notificacao.query.get(id)
        if not notificacao:
            return jsonify({"error": "Notificação não encontrada."}), 404

        notificacao.lida = True
        db.session.commit()

        return jsonify({"message": "Notificação marcada como lida."}), 200