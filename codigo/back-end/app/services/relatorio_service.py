from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from flask import jsonify
import os
from models import Relatorio
from database import db

class RelatorioService:
    @staticmethod
    def gerar_pdf(relatorio_id):
        # Busca o relatório no banco de dados
        relatorio = Relatorio.query.get(relatorio_id)
        if not relatorio:
            return jsonify({"error": "Relatório não encontrado."}), 404

        # Caminho para salvar o PDF
        uploads_dir = os.path.join(os.getcwd(), "uploads")
        os.makedirs(uploads_dir, exist_ok=True)  # Certifique-se de que a pasta existe
        pdf_path = os.path.join(uploads_dir, f"relatorio_{relatorio_id}.pdf")

        # Configurar o canvas do PDF
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Adicionar informações do relatório
        c.drawString(100, 750, f"Relatório ID: {relatorio.id}")
        c.drawString(100, 735, f"Vistoria ID: {relatorio.vistoria_id}")
        c.drawString(100, 720, f"Vistoriador ID: {relatorio.vistoriador_id}")
        c.drawString(100, 705, f"Data de Criação: {relatorio.data_geracao}")
        c.drawString(100, 690, f"Texto: {relatorio.texto}")

        # Adicionar fotos ao PDF
        y_position = 660
        for foto in relatorio.fotos:  # Assumindo que relatorio.fotos retorna uma lista de caminhos
            if os.path.exists(foto.nome_arquivo):  # Certifique-se de que `nome_arquivo` é o caminho da foto
                c.drawImage(foto.nome_arquivo, 100, y_position, width=200, height=150)
                y_position -= 160  # Espaço entre fotos

        # Finalizar o PDF
        c.save()

        return jsonify({"message": "PDF gerado com sucesso.", "path": pdf_path}), 200
