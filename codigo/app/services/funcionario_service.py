from services.notificacao_service import NotificacaoService
from models import Funcionario, Agendamento  # Importa os modelos ORM
from database import db  # Para gerenciar as transações do banco de dados
from flask import jsonify


class FuncionarioService:
    @staticmethod
    def vincular_vistoriador(creci, imobiliaria_id):
        """
        Vincula um Vistoriador a uma Imobiliária usando o CRECI.
        """
        # Verificar se o CRECI é válido
        vistoriador = Funcionario.query.filter_by(creci=creci, tipo="Vistoriador").first()
        if not vistoriador:
            return jsonify({"error": "Vistoriador com o CRECI fornecido não encontrado."}), 404

        # Verificar se já está vinculado a outra imobiliária
        if vistoriador.imobiliaria_id:
            return jsonify({"error": "Este Vistoriador já está vinculado a outra Imobiliária."}), 400

        # Vincular o Vistoriador à Imobiliária
        vistoriador.imobiliaria_id = imobiliaria_id
        db.session.commit()

        return jsonify({"message": "Vistoriador vinculado com sucesso.", "vistoriador": vistoriador.to_dict()}), 200

    @staticmethod
    def agendar_vistoria(id, data):
        """
        Agenda uma vistoria para o funcionário especificado.
        """
        # Busca o funcionário
        funcionario = Funcionario.query.get(id)
        if not funcionario:
            return jsonify({"error": "Funcionário não encontrado."}), 404

        # Validação de dados do agendamento
        if not all(k in data for k in ("vistoria_id", "data", "horario")):
            return jsonify({"error": "Dados incompletos para agendar vistoria."}), 400

        # Criação do agendamento
        agendamento = Agendamento(
            vistoria_id=data["vistoria_id"],
            data=data["data"],
            horario=data["horario"],
            funcionario_id=id
        )

        db.session.add(agendamento)
        db.session.commit()

        # Notificação
        mensagem = f"Vistoria agendada para {data['data']} às {data['horario']}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=id)

        return jsonify({"message": "Vistoria agendada com sucesso.", "agendamento": agendamento.to_dict()}), 200

    @staticmethod
    def reagendar_vistoria(id, data):
        """
        Reagenda uma vistoria para o funcionário especificado.
        """
        # Busca o agendamento
        agendamento = Agendamento.query.filter_by(id=data.get("agendamento_id"), funcionario_id=id).first()
        if not agendamento:
            return jsonify({"error": "Agendamento não encontrado ou não pertence ao funcionário."}), 404

        # Validação de dados do reagendamento
        if not all(k in data for k in ("nova_data", "novo_horario")):
            return jsonify({"error": "Dados incompletos para reagendar vistoria."}), 400

        # Atualização do agendamento
        agendamento.data = data["nova_data"]
        agendamento.horario = data["novo_horario"]
        db.session.commit()

        # Notificação
        mensagem = f"Vistoria reagendada para {data['nova_data']} às {data['novo_horario']}."
        NotificacaoService.criar_notificacao(mensagem, destinatario_id=id)

        return jsonify({"message": "Vistoria reagendada com sucesso.", "agendamento": agendamento.to_dict()}), 200
