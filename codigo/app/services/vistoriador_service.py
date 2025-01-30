from flask import jsonify
from models import Vistoria, Relatorio, Foto
from database import db
from datetime import datetime
import os

class VistoriadorService:
    @staticmethod
    def registrar_inspecao(id, data):
        # Validação de entrada
        if not all(k in data for k in ("vistoria_id", "texto", "fotos")):
            return jsonify({"error": "Dados incompletos para registrar a inspeção."}), 400

        # Busca a vistoria no banco de dados
        vistoria = Vistoria.query.filter_by(id=data["vistoria_id"], vistoriador_id=id).first()
        if not vistoria:
            return jsonify({"error": "Vistoria não encontrada ou não atribuída ao vistoriador."}), 404

        # Criação do relatório
        relatorio = Relatorio(
            vistoria_id=data["vistoria_id"],
            vistoriador_id=id,
            texto=data["texto"],
            data_geracao=datetime.utcnow()
        )
        db.session.add(relatorio)
        db.session.commit()  # Primeiro commit para gerar o ID do relatório

        # Salvar fotos associadas ao relatório
        uploads_dir = os.path.join(os.getcwd(), "uploads", "imagens")
        os.makedirs(uploads_dir, exist_ok=True)

        for foto in data["fotos"]:
            # Salvar a foto no diretório de uploads
            foto_path = os.path.join(uploads_dir, foto.filename)
            foto.save(foto_path)

            # Registrar a foto no banco de dados
            nova_foto = Foto(
                relatorio_id=relatorio.id,
                nome_arquivo=foto_path
            )
            db.session.add(nova_foto)

        db.session.commit()  # Commit final para salvar as fotos

        return jsonify({"message": "Relatório registrado com sucesso.", "relatorio": relatorio.to_dict()}), 200